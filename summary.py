import tiktoken
from langchain.chains import AnalyzeDocumentChain
from langchain.chains.summarize import load_summarize_chain
from langchain.llms import OpenAI

from read_pdf_text import get_pdf_text


def get_est_cost(model_name, split_docs):
    # the latest prices are here: https://openai.com/pricing#language-models
    price_map = {'gpt-4': 0.03, 'gpt-3.5-turbo': 0.002}
    model_price = price_map[model_name]
    enc = tiktoken.encoding_for_model(model_name)

    total_word_count = sum(len(pages.split()) for pages in split_docs)
    total_token_count = sum(len(enc.encode(pages)) for pages in split_docs)
    est_cost = total_token_count * model_price / 1000

    print(f'Total word count: {total_word_count}')
    print(f'Estimated tokens: {total_token_count}')
    print(f'Estimated cost of embedding: ${est_cost}')
    return total_word_count, total_token_count, est_cost


if __name__ == '__main__':
    model_name = 'gpt-3.5-turbo'
    doc_path_name = 'documents/ali_abdaal_blog.pdf'
    pages = get_pdf_text(doc_path_name)
    pages = pages.replace('\n', ' ') # for some reason each word was seperated by '\n' instead of ' '
    get_est_cost(model_name, pages)
    # print(len(set(pages.split(' '))))
    model = OpenAI(temperature=0)
    # print(dir(OpenAI))
    # signature = inspect.signature(load_qa_with_sources_chain).parameters
    # for name, parameter in signature.items():
    #     print(name, parameter.default, parameter.annotation, parameter.kind)
    summary_chain = load_summarize_chain(llm=model, chain_type='map_reduce')
    summarize_document_chain = AnalyzeDocumentChain(combine_docs_chain=summary_chain)
    try:
        print('output(AnalyzeDocumentChain):', summarize_document_chain.run(pages))
    except Exception as e:
        print('Exception:', e)
