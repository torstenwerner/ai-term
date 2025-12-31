<script>
    import {marked} from 'marked';
    import {askAi} from './lib/aiService';
    import Footer from './lib/Footer.svelte';
    import Loading from './lib/Loading.svelte';
    import SearchForm from './lib/SearchForm.svelte';
    import CopyToClipboard from './lib/CopyToClipboard.svelte';
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
     * Reference to the SearchForm component.
     */
    let searchFormComponent;

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
            response = result.toString();
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
            searchFormComponent?.focusInputElement();
        }
    }

    onMount(loadFromUrl);

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

    /**
     * Handles keyboard shortcuts.
     */
    function handleKeydown(event) {
        if (event.key === '/') {
            event.preventDefault();
            searchFormComponent?.focusInputElement();
        }
    }
</script>

<svelte:window on:popstate={loadFromUrl} on:keydown={handleKeydown}/>

<div class="app-container">
    <main>
        <SearchForm
            bind:type
            bind:prompt
            bind:this={searchFormComponent}
            {loading}
            onsubmit={handleSubmit}
        />

        {#if loading}
            <Loading/>
        {/if}

        {#if error}
            <div class="error">
                {error}
            </div>
        {/if}

        {#if response}
            <div class="response">
                {#await marked(response) then htmlResponse}
                    {@html htmlResponse}
                {/await}
            </div>
            <CopyToClipboard text={response} />
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
        padding: 0;
        width: 100%;
    }

    @media (max-width: 992px) {
        main {
            margin: 0 auto;
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
        padding: 1rem;
        border-radius: 4px;
        overflow-x: auto;
    }
</style>
