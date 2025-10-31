"""Query engine module for processing natural language queries and generating answers."""

from typing import List, Dict, Any, Optional, Tuple
from langchain.schema import Document
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.chains.qa_with_sources import load_qa_with_sources_chain


class QueryEngine:
    """Handles natural language queries and generates answers with citations."""
    
    def __init__(
        self,
        vector_store_manager,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: int = 500,
        top_k: int = 4
    ):
        """Initialize the query engine.
        
        Args:
            vector_store_manager: VectorStoreManager instance
            model: Name of the LLM model to use
            temperature: Temperature for response generation
            max_tokens: Maximum tokens in the response
            top_k: Number of documents to retrieve
        """
        self.vector_store_manager = vector_store_manager
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_k = top_k
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        # Create custom prompt template
        self.prompt_template = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Always provide the source of your information by mentioning the document name or source.

Context:
{context}

Question: {question}

Answer with source citations:"""
        
        self.PROMPT = PromptTemplate(
            template=self.prompt_template,
            input_variables=["context", "question"]
        )
    
    def query(self, question: str, score_threshold: Optional[float] = None) -> Dict[str, Any]:
        """Process a natural language query and return an answer with citations.
        
        Args:
            question: Natural language question
            score_threshold: Minimum relevance score for retrieved documents
            
        Returns:
            Dictionary containing answer, sources, and metadata
        """
        # Retrieve relevant documents with scores
        results = self.vector_store_manager.similarity_search(
            query=question,
            k=self.top_k,
            score_threshold=score_threshold
        )
        
        if not results:
            return {
                'answer': "I couldn't find any relevant information to answer your question.",
                'sources': [],
                'confidence': 0.0,
                'num_sources': 0
            }
        
        # Extract documents and scores
        documents, scores = zip(*results)
        
        # Create context from documents
        context = self._format_context(documents, scores)
        
        # Generate answer using LLM
        prompt = self.PROMPT.format(context=context, question=question)
        answer = self.llm.predict(prompt)
        
        # Extract source information
        sources = self._extract_sources(documents, scores)
        
        # Calculate overall confidence
        avg_confidence = sum(scores) / len(scores) if scores else 0.0
        
        return {
            'answer': answer.strip(),
            'sources': sources,
            'confidence': round(avg_confidence, 3),
            'num_sources': len(sources)
        }
    
    def query_with_retrieval_qa(self, question: str) -> Dict[str, Any]:
        """Alternative query method using RetrievalQA chain.
        
        Args:
            question: Natural language question
            
        Returns:
            Dictionary containing answer and metadata
        """
        retriever = self.vector_store_manager.as_retriever(k=self.top_k)
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.PROMPT}
        )
        
        result = qa_chain({"query": question})
        
        # Extract source information
        sources = []
        for doc in result.get('source_documents', []):
            sources.append({
                'file_name': doc.metadata.get('file_name', 'Unknown'),
                'source': doc.metadata.get('source', 'Unknown'),
                'content_preview': doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
            })
        
        return {
            'answer': result['result'],
            'sources': sources,
            'num_sources': len(sources)
        }
    
    def _format_context(self, documents: List[Document], scores: List[float]) -> str:
        """Format documents into context string with relevance scores.
        
        Args:
            documents: List of retrieved documents
            scores: List of relevance scores
            
        Returns:
            Formatted context string
        """
        context_parts = []
        
        for i, (doc, score) in enumerate(zip(documents, scores)):
            source = doc.metadata.get('file_name', 'Unknown source')
            content = doc.page_content
            context_parts.append(
                f"[Source {i+1}: {source} (Relevance: {score:.2%})]\n{content}\n"
            )
        
        return "\n".join(context_parts)
    
    def _extract_sources(
        self,
        documents: List[Document],
        scores: List[float]
    ) -> List[Dict[str, Any]]:
        """Extract source information from documents.
        
        Args:
            documents: List of retrieved documents
            scores: List of relevance scores
            
        Returns:
            List of source dictionaries
        """
        sources = []
        
        for doc, score in zip(documents, scores):
            source_info = {
                'file_name': doc.metadata.get('file_name', 'Unknown'),
                'source_path': doc.metadata.get('source', 'Unknown'),
                'relevance_score': round(score, 3),
                'chunk_id': doc.metadata.get('chunk_id', 'N/A'),
                'content_preview': doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
            }
            sources.append(source_info)
        
        return sources
    
    def get_relevant_documents(
        self,
        query: str,
        score_threshold: Optional[float] = None
    ) -> List[Tuple[Document, float]]:
        """Retrieve relevant documents without generating an answer.
        
        Args:
            query: Query string
            score_threshold: Minimum relevance score
            
        Returns:
            List of (Document, score) tuples
        """
        return self.vector_store_manager.similarity_search(
            query=query,
            k=self.top_k,
            score_threshold=score_threshold
        )
