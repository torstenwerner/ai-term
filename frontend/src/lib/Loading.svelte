<div class="loading">
    <div class="spinner"></div>
</div>

<style>
    .loading {
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
    }

    .spinner {
        width: 40px;
        height: 40px;
        border: 4px solid #f3f3f3;
        border-top: 4px solid #646cff;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    @media (prefers-color-scheme: dark) {
        .spinner {
            border-color: #333;
            border-top-color: #646cff;
        }
    }
</style>
