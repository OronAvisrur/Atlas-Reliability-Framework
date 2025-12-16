import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { searchBooks } from '../services/booksService';
import './QueryPage.css';

function QueryPage() {
  const [description, setDescription] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const handleSearch = async (e) => {
    e.preventDefault();

    if (!description.trim()) {
      setError('Please enter a book description');
      return;
    }

    try {
      setLoading(true);
      setError('');
      const data = await searchBooks(description);
      setResults(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Search failed. Please try again.');
      setResults(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="query-page">
      <header className="query-header">
        <div className="query-header-left">
          <h1>ATLAS</h1>
          <p>RELIABILITY FRAMEWORK</p>
        </div>
        <div className="query-header-right">
          <span className="username-display">Welcome, {user}</span>
          <button className="logout-button" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </header>

      <div className="query-content">
        <section className="query-section">
          <h2>Search Books</h2>
          <form onSubmit={handleSearch} className="search-form">
            <input
              type="text"
              className="search-input"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Describe the book you're looking for (e.g., 'action superhero books')"
              disabled={loading}
            />
            <button 
              type="submit" 
              className="search-button"
              disabled={loading}
            >
              {loading ? 'Searching...' : 'Search'}
            </button>
          </form>
          <p className="search-info">
            Our AI will extract keywords and search the Google Books database
          </p>
          {error && <div className="error-message">{error}</div>}
        </section>

        {loading && (
          <div className="loading-message">
            Searching books with AI-powered keyword extraction...
          </div>
        )}

        {results && (
          <section className="results-section">
            <h3 className="results-header">Search Results</h3>
            <p className="results-meta">
              Found {results.total_items} books using keywords: <strong>{results.query_keywords}</strong>
            </p>

            {results.items && results.items.length > 0 ? (
              <div className="books-grid">
                {results.items.map((book, index) => (
                  <div key={index} className="book-card">
                    {book.thumbnail && (
                      <img 
                        src={book.thumbnail} 
                        alt={book.title}
                        className="book-thumbnail"
                      />
                    )}
                    <h4 className="book-title">{book.title}</h4>
                    {book.authors && book.authors.length > 0 && (
                      <p className="book-authors">
                        by {book.authors.join(', ')}
                      </p>
                    )}
                    {book.categories && book.categories.length > 0 && (
                      <p className="book-categories">
                        {book.categories.join(', ')}
                      </p>
                    )}
                    {book.description && (
                      <p className="book-description">{book.description}</p>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-results">No books found. Try a different description.</div>
            )}
          </section>
        )}
      </div>
    </div>
  );
}

export default QueryPage;
