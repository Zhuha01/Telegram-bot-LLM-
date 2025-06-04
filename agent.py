from langchain.agents import initialize_agent
from langchain_core.tools import Tool

from decoding import vigenere_logic, defoe_logic, atbash_logic, tritemius_logic, caesar_logic
from information import cybersecurity_info,encryption_methods_info
from other import under,llm

system_prompt = """
You are a specialized assistant operating strictly within the following areas:

1. Cybersecurity — covering fundamental concepts, definitions, terminology, types of cyber threats, and protection methods.

2. Encryption methods — limited exclusively to the following five classical ciphers:
- Vigenère cipher
- Trithemius cipher
- Caesar cipher
- Daniel Defoe cipher
- Atbash cipher

Your capabilities and rules of operation:
- You must respond to user queries only if they clearly and explicitly relate to one of your areas of expertise.
- You must select the appropriate tool based on the query topic, strictly according to the tool selection criteria listed below.
- You must not answer or attempt to process any queries that fall outside of these domains.
- If a user query is unrelated, unclear, ambiguous, incomplete, or does not fit your scope — you must immediately run the Null tool and politely request a clearer, relevant, or more specific query.

No assumptions, improvisations, or responses beyond these guidelines are allowed. Be strict in following these rules.

Tool selection criteria:
- If the query is a general question about cybersecurity, cyber threats, definitions, or protection methods — use cybersecurity_info.
- If the query is a general question about the encryption methods listed above (their history, description, principles, or application cases) — use encryption_methods_info.
- If the query asks to encrypt or decrypt a message using the Vigenère cipher — use vigenere_tool.
- If the query asks to encrypt or decrypt a message using the Caesar cipher — use caesar_tool.
- If the query asks to encrypt or decrypt a message using the Daniel Defoe cipher — use defoe_cipher_tool.
 The user must provide an action (encrypt or decrypt), a message, and a keyword.
- If the query asks to encrypt or decrypt a message using the Trithemius cipher — use tritemius_tool.
- If the query asks to encrypt or decrypt a message using the Atbash cipher — use atbash_tool.
- In all other cases — including when the query:
    - Does not relate to cybersecurity or one of the five specified encryption methods.
    - Lacks clarity, is ambiguous, or cannot be reliably interpreted.
    - Contains unrelated, irrelevant, or unrecognized content.
— run the Null tool without exception.
"""

tools = [
    Tool.from_function(
        func=cybersecurity_info,
        name="cybersecurity_info",
        description="Use this tool to answer any general questions related to cybersecurity: definitions, types of cyber threats, basic principles of information protection, security practices, and preventive methods."
    ),
    Tool.from_function(
        func=encryption_methods_info,
        name="encryption_methods_info",
        description="Use this tool to respond to general informational queries about the five supported encryption methods: Vigenère, Trithemius, Caesar, Daniel Defoe, and Atbash ciphers. This includes their history, concept, use cases, and operational principles."
    ),
    Tool.from_function(
        func=vigenere_logic,
        name="vigenere_tool",
        description="Use this tool to encrypt or decrypt messages exclusively using the Vigenère cipher. Select this tool only when the user query explicitly requests encryption or decryption with the Vigenère method."
    ),
    Tool.from_function(
        func=caesar_logic,
        name="caesar_tool",
        description="Use this tool to encrypt or decrypt messages exclusively using the Caesar cipher. Select this tool only when the user query explicitly requests encryption or decryption with the Caesar method."
    ),
    Tool.from_function(
        func=defoe_logic,
        name="defoe_cipher_tool",
        description="Use this tool to encrypt or decrypt messages using the Daniel Defoe cipher. The user must clearly specify the operation (encrypt or decrypt), the message, and the keyword. Do not use this tool if any of these elements are missing."
    ),
    Tool.from_function(
        func=tritemius_logic,
        name="tritemius_tool",
        description="Use this tool to encrypt or decrypt messages exclusively using the Trithemius cipher. Select this tool only when the user explicitly requests encryption or decryption using the Trithemius method."
    ),
    Tool.from_function(
        func=atbash_logic,
        name="atbash_tool",
        description="Use this tool to encrypt or decrypt messages exclusively using the Atbash cipher. Select this tool only when the user explicitly requests encryption or decryption using the Atbash method."
    ),
    Tool.from_function(
        func=under,
        name="Null",
        description="Use this tool in all other cases when the user's query: does not relate to cybersecurity or one of the five supported encryption methods; lacks clarity; includes irrelevant, unrelated, or unrecognized terms; or does not make sense. This is your universal fallback tool."
    )
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=False,
    system_message=system_prompt
)