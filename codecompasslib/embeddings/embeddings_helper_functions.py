import numpy as np
from gensim.models.keyedvectors import KeyedVectors
from sentence_transformers import SentenceTransformer
from langchain_community.embeddings import OllamaEmbeddings
from gensim.models import KeyedVectors
import openai

def load_word2vec_model():
    """
    Load pre-trained Word2Vec model for the Software Engineering Domain.

    This function loads a pre-trained Word2Vec model that has been trained on 15GB of Stack Overflow posts.
    The model is stored in the file 'SO_vectors_200.bin' in the 'codecompasslib/PretrainedModels' directory.

    Returns:
        word_vect (gensim.models.keyedvectors.Word2VecKeyedVectors): The loaded Word2Vec model.

    Citation:
        Efstathiou Vasiliki, Chatzilenas Christos, & Spinellis Diomidis. (2018). Word Embeddings for the Software Engineering Domain [Data set]. Zenodo. https://doi.org/10.5281/zenodo.1199620
    """
    word_vect = KeyedVectors.load_word2vec_format("./codecompasslib/PretrainedModels/SO_vectors_200.bin", binary=True)
    return word_vect

# Vectorizing text using domain specific word2vec model
def vectorize_text(text, word_vect):
    """
    Vectorizes the given text by computing the average of word vectors.

    Parameters:
        text (str): The input text to be vectorized.
        word_vect (WordVectorKeyedVectors): The word vector model used for vectorization.

    Returns:
        numpy.ndarray: The vector representation of the input text.

    """
    vector_sum = np.zeros(word_vect.vector_size)  # Initialize an array to store the sum of word vectors
    count = 0  # Initialize a count to keep track of the number of words found in the vocabulary
    for word in text.split():
        if word in word_vect.key_to_index:  # Check if the word is in the vocabulary
            vector_sum += word_vect[word]  # Add the word vector to the sum
            count += 1  # Increment the count
    if count > 0:
        return vector_sum / count  # Return the average of word vectors
    else:
        return vector_sum  # Return the zero vector if no words are found in the vocabulary

def generate_openAI_embeddings(strings_to_embed, client):
    """
    Generates OpenAI embeddings for the given strings using the specified OpenAI model.

    Args:
        strings_to_embed (list): A list of strings to generate embeddings for.
        client: The OpenAI client object used to make API requests.

    Returns:
        dict: A dictionary containing the embeddings generated by OpenAI.

    Raises:
        OpenAIException: If there is an error while making the API request.

    """
    response = client.embeddings.create(
        input=strings_to_embed,
        model="text-embedding-3-large",  # You can choose the model you prefer
        dimensions=256  # You can choose the number of dimensions you prefer
    )
    return response

def generate_sentence_transformer_embeddings(text):
    """
    Generates Sentence Transformer embeddings for the given text.

    Parameters:
    text (str): The input text to generate embeddings for.

    Returns:
    embedding (numpy.ndarray): The Sentence Transformer embeddings for the input text.
    """

    # Load a pre-trained Sentence Transformer model
    model_name = 'stsb-roberta-base'
    model = SentenceTransformer(model_name)
    embedding = model.encode(text)
    return embedding

def generate_llama_embeddings(text):
    """
    Generates embeddings for the given text using the OllamaEmbeddings model.
    
    Args:
        text (str): The input text for which embeddings need to be generated.
        
    Returns:
        query_result (list): A list of embeddings for the input text.
    """
    embeddings_model = OllamaEmbeddings(model='ollama-7b', device='gpu') # select the model you have installed on your machine
    query_result = embeddings_model.embed_query(text)
    return query_result
