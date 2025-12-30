<script>
    import {marked} from 'marked';
    import {askAi} from './lib/aiService';
    import Footer from './lib/Footer.svelte';
    import Loading from './lib/Loading.svelte';
    import TypeSelector from './lib/TypeSelector.svelte';
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

    /**
     * Fetches AI response without modifying browser history.
     */
    async function fetchResponse() {
        loading = true;
        response = ""
        error = null;
        try {
            // Update window title
            document.title = prompt || 'dictionary';

            const result = await askAi(type, prompt);
            response = await marked(result.toString());
        } catch (e) {
            error = e instanceof Error ? e.message : 'An error occurred';
        } finally {
            loading = false;
        }
    }

    /**
     * Reads URL parameters and updates the state accordingly.
     */
    function loadFromUrl() {
        const urlParams = new URLSearchParams(window.location.search);
        type = urlParams.get('type') || "DICTIONARY_EN";
        const urlPrompt = urlParams.get('prompt');
        if (urlPrompt) {
            prompt = urlPrompt;
            fetchResponse();
        } else {
            // Clear response when navigating to a URL without a prompt
            response = '';
            error = null;
            document.title = 'dictionary';
        }
    }

    onMount(loadFromUrl);

    /**
     * Returns a placeholder text for the input element depending on the search type.
     */
    function placeholder() {
        switch (type) {
            case 'DICTIONARY_EN':
                return 'enunciate';
            case 'ENCYCLOPEDIA_EN':
                return 'Aphrodite';
            case 'ENCYCLOPEDIA_DE':
                return 'Mythologie'
        }
        return '';
    }

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
        // Update URL with the new prompt
        const url = new URL(window.location.href);
        url.searchParams.set('type', type);
        if (prompt) {
            url.searchParams.set('prompt', prompt);
        } else {
            url.searchParams.delete('prompt');
        }
        window.history.pushState({}, '', url);

        // Fetch the response
        await fetchResponse();
    }
</script>

<svelte:window on:popstate={loadFromUrl} />

<div class="app-container">
    <main>
        <form on:submit|preventDefault={handleSubmit}>
            <TypeSelector bind:type disabled={loading} onChange={handleTypeChange} />
            <div class="input-group">
                <input
                        type="text"
                        bind:value={prompt}
                        bind:this={inputElement}
                        on:click={handleInputClick}
                        placeholder={placeholder()}
                        title="Enter a term"
                        disabled={loading}
                />
                <button type="submit" disabled={loading || !prompt}>
                    {loading ? 'Please wait' : 'Submit'}
                </button>
            </div>
        </form>

        {#if loading}
            <Loading />
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

    input {
        flex: 1;
        padding: 0.5rem;
        font-size: 1rem;
        background-color: unset;
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
        padding: 1rem;
        border-radius: 4px;
        overflow-x: auto;
    }
</style>
