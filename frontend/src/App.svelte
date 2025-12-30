<script>
    import {marked} from 'marked';
    import {askAi} from './lib/aiService';
    import Footer from './lib/Footer.svelte';
    import {onMount} from 'svelte';

    /**
     * Represents the search type e.g. dictionary, encyclopedia.
     */
    let type = '';

    /**
     * Represents the user-provided term.
     */
    let prompt = '';

    /**
     * The HTML response from the AI-backed backend service.
     */
    let response = '';

    /**
     * The state of the loading indicator.
     */
    let loading = false;

    /**
     * Optional error message.
     */
    let error = null;

    /**
     * Reference to the input element in the DOM.
     */
    let inputElement;

    onMount(() => {
        const urlParams = new URLSearchParams(window.location.search);
        type = urlParams.get('type') || "DICTIONARY_EN";
        const urlPrompt = urlParams.get('prompt');
        if (urlPrompt) {
            prompt = urlPrompt;
            handleSubmit();
        }
    });

    /**
     * Reacts to a change of the search type.
     */
    function handleTypeChange() {
        inputElement?.focus();
        inputElement?.select();
    }

    /**
     * Reacts to a click on the input element.
     */
    function handleInputClick() {
        inputElement?.select();
    }

    /**
     * Handles the form submission by updating the URL and fetching the AI response.
     *
     * @return {Promise<void>} A promise that resolves when the process is complete.
     */
    async function handleSubmit() {
        loading = true;
        response = ""
        error = null;
        try {
            // Update URL with the new prompt
            const url = new URL(window.location.href);
            url.searchParams.set('type', type);
            if (prompt) {
                url.searchParams.set('prompt', prompt);
            } else {
                url.searchParams.delete('prompt');
            }
            window.history.pushState({}, '', url);

            const result = await askAi(type, prompt);
            response = await marked(result.toString());
        } catch (e) {
            error = e instanceof Error ? e.message : 'An error occurred';
        } finally {
            loading = false;
        }
    }
</script>

<div class="app-container">
    <main>
        <form on:submit|preventDefault={handleSubmit}>
            <select bind:value={type} on:change={handleTypeChange} disabled={loading}>
                <option value="DICTIONARY_EN">Dictionary English</option>
                <option value="ENCYCLOPEDIA_EN">Encyclopedia English</option>
                <option value="ENCYCLOPEDIA_DE">Encyclopedia German</option>
            </select>
            <div class="input-group">
                <input
                        type="text"
                        bind:value={prompt}
                        bind:this={inputElement}
                        on:click={handleInputClick}
                        placeholder="Mars"
                        title="Enter a term"
                        disabled={loading}
                />
                <button type="submit" disabled={loading || !prompt}>
                    {loading ? 'Please wait' : 'Submit'}
                </button>
            </div>
        </form>

        {#if loading}
            <div class="loading">
                <div class="spinner"></div>
            </div>
        {/if}

        {#if error}
            <div class="error">
                {error}
            </div>
        {/if}

        {#if response}
            <div class="response">
                {@html response}
            </div>
        {/if}
    </main>
    <Footer/>
</div>

<style>
    .app-container {
        min-height: 80vH;
        display: flex;
        flex-direction: column;
    }

    main {
        margin: 2rem auto;
        padding: 0 1rem;
        width: 100%;
    }

    .input-group {
        display: flex;
        gap: 1rem;
        margin-bottom: 2rem;
    }

    select {
        padding: 0.5rem;
        font-size: 1rem;
        border: 1px solid #ccc;
        border-radius: 4px;
        margin-bottom: 1rem;
        width: max(250px, 33%);
    }

    input {
        flex: 1;
        padding: 0.5rem;
        font-size: 1rem;
        border: 1px solid #ccc;
        border-radius: 4px;
    }

    button {
        padding: 0.5rem 1rem;
        font-size: 1rem;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }

    button:disabled {
        background-color: #cccccc;
        cursor: not-allowed;
    }

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

    .error {
        color: #ff3e00;
        margin-bottom: 1rem;
    }

    .response {
        padding: 1rem;
        border-radius: 4px;
        border: 1px solid #eee;
    }

    @media (prefers-color-scheme: dark) {
        .response {
            border-color: #555;
        }
    }

    .response :global(h1),
    .response :global(h2),
    .response :global(h3) {
        margin-top: 0;
    }

    .response :global(p) {
        margin-bottom: 1rem;
    }

    .response :global(pre) {
        /*background-color: #f1f1f1;*/
        padding: 1rem;
        border-radius: 4px;
        overflow-x: auto;
    }
</style>
