import openai
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class LLM(object):
    def __init__(self, openai_key: str):
        openai.api_key = openai_key
        self.context = []
        self.system_context = [
            {"role": "system", "content": "Don't say that you are an AI model"},
            {
                "role": "system",
                "content": speech_configuration.actor,
            },
        ]
        self.model = "gpt-3.5-turbo"
        self.tokens_limit = 4096
        self.tokens = 0
        for msg in self.system_context:
            self.tokens += self.estimate_tokens(msg["content"])

    def ask(self, prompt):
        # remove conetxt when tokens limit is reached
        estimated_tokens = self.estimate_tokens(prompt)
        if estimated_tokens > self.tokens_limit:
            # TODO: truncate question?
            logger.error("Message is too long")
            return None

        self.tokens += estimated_tokens
        while self.tokens_limit < self.tokens:
            self.tokens -= self.estimate_tokens(self.context.pop(0)["message"])

        self.context.append({"role": "user", "content": prompt})

        messages = []
        messages.extend(self.system_context)
        messages.extend(self.context)

        ai_response = openai.ChatCompletion.create(
            model=self.model,
            # max_tokens: the maximum number of words or parts of words (tokens) the assistant is allowed to use in its response
            max_tokens=500,
            # temperature: controls how creative or random the digital assistant’s responses will be. A lower number (like 0.05) means the assistant will be more focused and consistent, while a higher number would make the assistant more creative and unpredictable
            temperature=0.7,
            messages=messages,
        )
        # Get response
        # {
        #     "id": "chatcmpl-6viHI5cWjA8QWbeeRtZFBnYMl1EKV",
        #     "object": "chat.completion",
        #     "created": 1679212920,
        #     "model": "gpt-4-0314",
        #     "usage": {
        #         "prompt_tokens": 21,
        #         "completion_tokens": 5,
        #         "total_tokens": 26
        #     },
        #     "choices": [
        #         {
        #             "message": {
        #                 "role": "assistant",
        #                 "content": "GPT-4 response returned here"
        #             },
        #             "finish_reason": "stop",
        #             "index": 0
        #         }
        #     ]
        # }

        # Self response for context
        self.context.append(ai_response["choices"][0]["message"])

        response_text = ai_response["choices"][0]["message"]["content"].strip()
        logger.debug("Got the OpenAI response: %s", ai_response)
        return response_text