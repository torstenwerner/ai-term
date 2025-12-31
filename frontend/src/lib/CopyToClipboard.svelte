<script>
    /**
     * The text to copy to the clipboard.
     */
    export let text = '';

    /**
     * Indicates if the copy button was just clicked.
     */
    let copyClicked = false;

    /**
     * Copies the text to the clipboard.
     */
    async function copyToClipboard() {
        try {
            await navigator.clipboard.writeText(text);
            copyClicked = true;
            setTimeout(() => {
                copyClicked = false;
            }, 750);
        } catch (e) {
            console.error('Failed to copy to clipboard:', e);
        }
    }
</script>

<div class="copy-container" title="Copy to clipboard">
    <svg
        class="copy-icon"
        class:clicked={copyClicked}
        on:click={copyToClipboard}
        xmlns="http://www.w3.org/2000/svg"
        width="20"
        height="20"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
    >
        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
    </svg>
    {#if copyClicked}
        <span class="copy-text">Copied to clipboard</span>
    {/if}
</div>

<style>
    .copy-container {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-top: 1rem;
    }

    .copy-icon {
        cursor: pointer;
        color: #666;
        transition: color 0.2s ease;
    }

    .copy-icon:hover {
        color: #333;
    }

    .copy-icon.clicked {
        color: #4CAF50;
        transform: scale(0.9);
    }

    .copy-text {
        font-size: 0.875rem;
        color: #4CAF50;
    }

    @media (prefers-color-scheme: dark) {
        .copy-icon {
            color: #999;
        }

        .copy-icon:hover {
            color: #ccc;
        }

        .copy-icon.clicked {
            color: #4CAF50;
        }

        .copy-text {
            color: #4CAF50;
        }
    }
</style>
