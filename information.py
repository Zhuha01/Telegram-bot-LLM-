from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_core.prompts import PromptTemplate

from BD import vectors
from other import llm

custom_prompts = {
    "cybersecurity": PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are an assistant specializing strictly in cybersecurity topics. 

Using **only the cybersecurity description provided below**, carefully analyze the user's question and give a clear, precise, and relevant answer based solely on the information from the description.

If the description does not contain enough data to fully answer the question, state this directly and politely ask the user to provide more specific details or clarify their request.

Do not use any external knowledge or assumptions. Operate strictly within the scope of the provided description.

Cybersecurity Description:
{context}

User's Question:
{question}

Answer:
"""
    ),

    "encryption": PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are an assistant specializing exclusively in the following five encryption methods:
   - Vigenère cipher
   - Trithemius cipher
   - Caesar cipher
   - Daniel Defoe cipher
   - Atbash cipher

Using **only the encryption methods description provided below**, carefully review the user's question and provide a clear, accurate, and relevant answer based strictly on the description content.

If the description does not provide enough information to fully answer the question, state this openly and politely ask the user to clarify their query or provide more specific details.

Do not use any external information, guesses, or assumptions. Work strictly within the given description.

Encryption Methods Description:
{context}

User's Question:
{question}

Answer:
"""
    )
}

qa_chains = {}

for topic in ["cybersecurity", "encryption"]:
    retriever = vectors.as_retriever(search_kwargs={"filter": {"topic": topic}})
    prompt = custom_prompts[topic]
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt}
    )
    qa_chains[topic] = qa_chain

def cybersecurity_info(query: str) -> str:
    return qa_chains["cybersecurity"].invoke(query)

def encryption_methods_info(query: str) -> str:
    return qa_chains["encryption"].invoke(query)



