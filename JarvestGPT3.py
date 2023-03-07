
import numpy as np
import pandas as pd

from abc import ABC, abstractmethod
import os
import openai
#os.environ['OPEN_API_KEY'] = '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'
sid = 'SK96cff15bd5c6e85ef46c0cd683cceb99'
secret = 'hSOkDQ7Blm2UYKraJeDXHExe3P6ALqvs'

hyperparameters = {}

# class JarvestGPT3(ABC):
#     @abstractmethod
#     def prompt(self):
#         pass

class JarvestPromptGenerator:

    openai.api_key = os.getenv('OPENAI_API_KEY')
    def __init__(self, params = hyperparameters):

        self.hyperparameters = params
        self.stop_sequence = "\\n###\\n"
        self.conv_cache = ""


    def get_prompt_types(self):
        return ['general','simplify','sum_link','sum_book']

    def add_cache(self, prompt):
        self.conv_cache += "\n###\n"
        self.conv_cache += prompt
        self.conv_cache += "\n###\n"

    def prompt(self, prompt, type = 'general', cache = True, **params):

        if cache:
            self.add_cache(prompt)
            prompt = self.conv_cache


        if type == 'general':
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"{prompt}",
                temperature=0.6,
                max_tokens=3000,
                top_p=1,
                frequency_penalty=1,
                presence_penalty=.50
            )
            # implementation of prompt generation goes here
            response = list(response.values())[4][0]['text']
            response = '\n'.join([x.strip() for x in response.split('\n')])
            self.add_cache(response)
            return response

        else:
            func_dict = {
                'simplify': self.simplify_text,
                'sum_link': self.summarize_link,
                'sum_book': self.summarize_book
            }
            try:
                engine = func_dict[type]
                return engine(prompt, **params)
            except:
                print('request type invalid')

    def simplify_text(self):
        pass

    def summarize_text(self, prompt, n = 1, **params):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"""###
            Rewrite the following text and summarize it to be more clear and concise
            {prompt}

            Then give me {n} main takeaway from it
            ###

            """,
            **params
            )

        # implementation of prompt generation goes here
        response = list(response.values())[4][0]['text']
        response = '\n'.join([x.strip() for x in response.split('\n')])
        self.add_cache(response)
        return response

    def summarize_link(self, prompt, n = 5, **params):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"""###
            analyze and summarize the following article in the following link:
            {prompt}

            Then give me {n} main takeaway from it

            Here is {n} takeaways from the given link:

            ###
            """,
            **params,
            temperature=0.3,
            max_tokens=3000,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=.50

            )
        # implementation of prompt geAneration goes here
        response = list(response.values())[4][0]['text']
        response = '\n'.join([x.strip() for x in response.split('\n')])
        self.add_cache(response)
        return response

    def summarize_book(self, book, author = "the most recent author", n = 5,  **params):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"""###
            analyze and summarize the conclusion following book {book}:
            {book}
            author: {author}

            Then give me up to {n} main takeaway from it, followed by a summary conclusion
            ###
            Here is {n} main takeaway(s) from {book}:

            """,
            temperature=0.1,
            max_tokens=3000,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=.50
            )
        # implementation of prompt generation goes here
        response = list(response.values())[4][0]['text']
        response = '\n'.join([x.strip() for x in response.split('\n')])
        self.add_cache(response)
        return response

    def create_linked_in_post(self, prompt, source_type = None,  **params):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"""###
            create a LinkedIN post about {prompt}
            with the following structure:

            Intro

            Body

            Outro

            ###
            {prompt}
            """,
            temperature=0.5,
            max_tokens=3000,
            top_p=2,
            frequency_penalty=0,
            presence_penalty=0
        )
        # implementation of prompt generation goes here
        response = list(response.values())[4][0]['text']
        response = '\n'.join([x.strip() for x in response.split('\n')])
        self.add_cache(response)
        return response


