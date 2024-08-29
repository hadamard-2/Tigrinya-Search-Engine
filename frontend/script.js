document.getElementById('submitQuery').addEventListener('click', function() {
    const query = document.getElementById('queryInput').value;

    fetch('http://127.0.0.1:5000/preprocess', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Search Results:', data.tokens);
        // Display the preprocessed tokens in your UI as needed
    })
    .catch(error => console.error('Error:', error));
});
