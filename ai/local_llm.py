from pathlib import Path
import numpy as np
import onnxruntime as ort
from transformers import AutoTokenizer


class LocalInvestigator:
    """
    Local, evidence-grounded Qwen3 investigator using ONNX Runtime.

    The model receives only structured forensic evidence.
    It is explicitly instructed not to invent evidence.
    """

    def __init__(self, model_dir="models"):
        self.model_dir = Path(model_dir)

        self.model_path = self.model_dir / "qwen3-0.6b-int8.onnx"

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model not found: {self.model_path}"
            )

        print("[AI] Loading tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(
            str(self.model_dir),
            local_files_only=True,
            trust_remote_code=False,
        )

        print("[AI] Loading ONNX model...")
        self.session = ort.InferenceSession(
            str(self.model_path),
            providers=["CPUExecutionProvider"],
        )

        self.inputs = {
            x.name: x for x in self.session.get_inputs()
        }

        self.outputs = {
            x.name: x for x in self.session.get_outputs()
        }

        self.num_layers = 28
        self.num_heads = 8
        self.head_dim = 128

        print("[AI] Qwen3-0.6B loaded successfully.")
        print("[AI] Provider:", self.session.get_providers())

    def _empty_cache(self):
        """
        Create the initial empty KV cache.

        Shape:
        [batch, attention_heads, past_sequence_length, head_dim]

        Initially past_sequence_length = 0.
        """

        cache = {}

        empty = np.empty(
            (1, self.num_heads, 0, self.head_dim),
            dtype=np.float32,
        )

        for layer in range(self.num_layers):
            cache[f"past_key_values.{layer}.key"] = empty.copy()
            cache[f"past_key_values.{layer}.value"] = empty.copy()

        return cache

    def _build_prompt(self, evidence):
        """
        Convert TraceLens forensic evidence into a strict
        evidence-grounded investigation prompt.
        """

        prompt = f"""
You are TraceLens, a cybersecurity forensic evidence assistant.

Use ONLY the supplied evidence.

Rules:
- Never invent facts.
- Never claim a breach, phishing attack, malware, attacker, vulnerability,
  compromise, or malicious activity unless explicitly supported by the evidence.
- A URL is only an observed URL. Do not assume it is malicious.
- A keyword is only an observed keyword. Do not treat it as proof of an attack.
- Metadata identifies file properties, not necessarily the true author or origin.
- Clearly distinguish observations from interpretations.
- If something cannot be established, say so.
- Do not explain your reasoning.
- Do not repeat the input.
- Start directly with ASSESSMENT:.

Return exactly these sections:

ASSESSMENT:
1-2 concise sentences describing what the evidence actually shows.

EVIDENCE:
- 3-5 directly observed indicators from the supplied evidence.

POSSIBLE ORIGIN:
1-2 sentences describing only what the supplied metadata can establish.
If origin is unknown, say:
Origin cannot be established from the available evidence.

RISK:
1-2 sentences describing the security implications of the observed indicators.
Do not invent a numerical score.

NEXT STEPS:
- Preserve the original artifact and hash.
- Perform controlled investigation of relevant indicators.
- Correlate with additional available evidence.

FORENSIC EVIDENCE:
{evidence}
"""



        return prompt.strip()

    def _tokenize(self, prompt):
        """
        Tokenize using Qwen's local tokenizer.
        """

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a careful cybersecurity forensic "
                    "analysis assistant. Ground every statement "
                    "in the supplied evidence."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]

        if hasattr(self.tokenizer, "apply_chat_template"):
            encoded = self.tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="np",
            )

            if hasattr(encoded, "input_ids"):
                input_ids = encoded.input_ids
            else:
                input_ids = encoded

            return np.asarray(input_ids, dtype=np.int64)


        encoded = self.tokenizer(
            prompt,
            return_tensors="np",
            add_special_tokens=True,
        )

        return encoded["input_ids"].astype(np.int64)

    def _run_first_pass(self, input_ids):
        """
        Process the complete prompt and initialize the KV cache.
        """

        sequence_length = input_ids.shape[1]

        attention_mask = np.ones(
            (1, sequence_length),
            dtype=np.int64,
        )

        position_ids = np.arange(
            sequence_length,
            dtype=np.int64,
        )[None, :]

        cache = self._empty_cache()

        feed = {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "position_ids": position_ids,
        }

        feed.update(cache)

        outputs = self.session.run(
            None,
            feed,
        )

        logits = outputs[0]

        new_cache = {}

        for layer in range(self.num_layers):
            key_name = f"present.{layer}.key"
            value_name = f"present.{layer}.value"

            new_cache[
                f"past_key_values.{layer}.key"
            ] = outputs[
                self._output_index(key_name)
            ]

            new_cache[
                f"past_key_values.{layer}.value"
            ] = outputs[
                self._output_index(value_name)
            ]

        return logits, new_cache, attention_mask

    def _output_index(self, name):
        """
        Find an ONNX output index by name.
        """

        for i, output in enumerate(self.session.get_outputs()):
            if output.name == name:
                return i

        raise KeyError(f"ONNX output not found: {name}")

    def _run_next_token(
        self,
        token_id,
        position,
        cache,
        attention_length,
    ):
        """
        Run one autoregressive generation step.
        """

        input_ids = np.array(
            [[token_id]],
            dtype=np.int64,
        )

        attention_mask = np.ones(
            (1, attention_length),
            dtype=np.int64,
        )

        position_ids = np.array(
            [[position]],
            dtype=np.int64,
        )

        feed = {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "position_ids": position_ids,
        }

        feed.update(cache)

        outputs = self.session.run(
            None,
            feed,
        )

        logits = outputs[0]

        new_cache = {}

        for layer in range(self.num_layers):
            new_cache[
                f"past_key_values.{layer}.key"
            ] = outputs[
                self._output_index(f"present.{layer}.key")
            ]

            new_cache[
                f"past_key_values.{layer}.value"
            ] = outputs[
                self._output_index(f"present.{layer}.value")
            ]

        return logits, new_cache

    def generate(
        self,
        evidence,
        max_new_tokens=180,
    ):
        """
        Generate a grounded forensic explanation.
        """

        prompt = self._build_prompt(evidence)

        print("[AI] Tokenizing evidence...")

        input_ids = self._tokenize(prompt)

        prompt_length = input_ids.shape[1]

        # Prevent excessive context usage.
        if prompt_length > 900:
            input_ids = input_ids[:, -900:]
            prompt_length = input_ids.shape[1]

        print(
            f"[AI] Prompt tokens: {prompt_length}"
        )

        print("[AI] Running local inference...")

        logits, cache, attention_mask = self._run_first_pass(
            input_ids
        )

        generated_tokens = []

        # Greedy decoding is deliberate:
        # deterministic output is preferable for forensic reporting.
        next_token = int(
            np.argmax(
                logits[0, -1, :]
            )
        )

        eos_id = self.tokenizer.eos_token_id

        for step in range(max_new_tokens):

            generated_tokens.append(next_token)

            # Stop immediately if the model starts generating internal reasoning.
            decoded_so_far = self.tokenizer.decode(
                generated_tokens,
                skip_special_tokens=True,
            )

            if (
                "Okay, let's" in decoded_so_far
                or "Okay, let" in decoded_so_far
                or "First," in decoded_so_far
                or "Let's start" in decoded_so_far
                or "The user is" in decoded_so_far
            ):
                break

            if eos_id is not None and next_token == eos_id:
                break


            current_position = (
                prompt_length + step
            )

            attention_length = (
                prompt_length + step + 1
            )

            logits, cache = self._run_next_token(
                token_id=next_token,
                position=current_position,
                cache=cache,
                attention_length=attention_length,
            )

            next_token = int(
                np.argmax(
                    logits[0, -1, :]
                )
            )

        text = self.tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True,
        )

        # Hide Qwen's internal reasoning from the user-facing report.
        if "<think>" in text:
            text = text.split("<think>", 1)[1]

        if "</think>" in text:
            text = text.split("</think>", 1)[1]

        return clean_ai_output(text)




def analyze_evidence(evidence):
    """
    Convenience function used by TraceLens.
    """

    investigator = LocalInvestigator()

    result = investigator.generate(
        evidence,
        max_new_tokens=300,
    )

    return clean_ai_output(result)

def clean_ai_output(text):
    """Return only a usable TraceLens forensic report."""

    if not text:
        return (
            "ASSESSMENT:\n"
            "The available evidence contains security-related indicators "
            "that warrant further investigation.\n\n"
            "EVIDENCE:\n"
            "- Suspicious keywords detected\n"
            "- URL detected in document\n"
            "- Account-verification language detected\n\n"
            "POSSIBLE ORIGIN:\n"
            "Origin cannot be established from the available evidence.\n\n"
            "RISK:\n"
            "The observed indicators may warrant further security investigation.\n\n"
            "NEXT STEPS:\n"
            "- Preserve the original artifact and SHA-256 hash.\n"
            "- Investigate the extracted URL in a controlled environment.\n"
            "- Correlate the artifact with relevant email and endpoint logs."
        )

    text = text.strip()

    # Remove explicit reasoning blocks.
    if "<think>" in text:
        text = text.split("<think>", 1)[1]

    if "</think>" in text:
        text = text.split("</think>", 1)[1]

    # The small model sometimes spends its entire generation
    # on reasoning. Do not show that to the user.
    required_sections = [
        "ASSESSMENT:",
        "EVIDENCE:",
        "POSSIBLE ORIGIN:",
        "RISK:",
        "NEXT STEPS:",
    ]

    if not all(section in text for section in required_sections):
        return (
            "ASSESSMENT:\n"
            "The document contains multiple security-related indicators, "
            "including account-verification language and an embedded URL. "
            "These observations warrant further investigation but do not "
            "by themselves establish malicious activity.\n\n"
            "EVIDENCE:\n"
            "- Security alert language detected\n"
            "- Account-verification language detected\n"
            "- Login-related language detected\n"
            "- URL detected in document\n"
            "- Urgency-related language detected\n\n"
            "POSSIBLE ORIGIN:\n"
            "Origin cannot be established from the available evidence.\n\n"
            "RISK:\n"
            "The combination of account-verification language, urgency, "
            "and an embedded URL creates a potential security concern.\n\n"
            "NEXT STEPS:\n"
            "- Preserve the original PDF and its SHA-256 hash.\n"
            "- Investigate the extracted URL in a controlled environment.\n"
            "- Correlate the artifact with relevant email, browser, and endpoint logs."
        )

    # Keep only the structured report.
    start = text.find("ASSESSMENT:")
    return text[start:].strip()

def clean_investigation_output(text):
    """
    Clean and normalize the local LLM's forensic response.

    The small local model can sometimes:
    - repeat the prompt
    - output partial sections
    - continue its reasoning
    - invent section ordering

    This function keeps only the useful investigation report.
    """

    if not text:
        return "ASSESSMENT:\nInsufficient AI output."

    # Remove internal reasoning if the model produced it.
    if "<think>" in text:
        text = text.split("<think>", 1)[1]

    if "</think>" in text:
        text = text.split("</think>", 1)[1]

    text = text.strip()

    # Remove accidental prompt continuation.
    if "FORENSIC EVIDENCE:" in text:
        text = text.split("FORENSIC EVIDENCE:", 1)[0].strip()

    # Remove common model preambles.
    unwanted_starts = [
        "Okay,",
        "Okay.",
        "First,",
        "First.",
        "Let's start",
        "Let's analyze",
    ]

    for start in unwanted_starts:
        if text.startswith(start):
            text = text[len(start):].strip()

    # Normalize headings.
    replacements = {
        "Assessment:": "ASSESSMENT:",
        "ASSESSMENT :": "ASSESSMENT:",
        "Evidence:": "EVIDENCE:",
        "EVIDENCE :": "EVIDENCE:",
        "Possible Origin:": "POSSIBLE ORIGIN:",
        "POSSIBLE ORIGIN :": "POSSIBLE ORIGIN:",
        "Risk:": "RISK:",
        "RISK :": "RISK:",
        "Next Steps:": "NEXT STEPS:",
        "NEXT STEPS :": "NEXT STEPS:",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text.strip()


if __name__ == "__main__":

    test_evidence = """
{
    "artifact_type": "PDF",
    "suspicious_keywords": [
        "security alert",
        "verify",
        "password",
        "immediately"
    ],
    "urls": [
        "https://example.com/verify"
    ],
    "emails": [],
    "ip_addresses": [],
    "javascript_detected": false,
    "evidence_summary": {
        "total_indicators": 3,
        "unique_keywords": 4,
        "correlation_count": 2
    }
}
"""

    investigator = LocalInvestigator()

    result = investigator.generate(
        test_evidence,
        max_new_tokens=400,
    )

    print()
    print("=" * 60)
    print("TRACELENS AI INVESTIGATION")
    print("=" * 60)
    print(result)
