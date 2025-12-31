<script>
    import {createEventDispatcher} from 'svelte';
    import TypeSelector from './TypeSelector.svelte';

    const dispatch = createEventDispatcher();

    /**
     * Represents the search type e.g. dictionary, encyclopedia.
     */
    export let type = '';

    /**
     * Represents the user-provided term.
     */
    export let prompt = '';

    /**
     * The state of the loading indicator.
     */
    export let loading = false;

    /**
     * Reference to the input element in the DOM.
     */
    let inputElement;

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
     * Focuses the input element and selects all its text.
     */
    export function focusInputElement() {
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
     * Handles the form submission.
     */
    function handleSubmit() {
        // Dispatch a custom event that the parent can listen to
        dispatch('submit', { type, prompt });
    }
</script>

<form on:submit|preventDefault={handleSubmit}>
    <TypeSelector bind:type disabled={loading} onChange={focusInputElement}/>
    <div class="input-group">
        <input
                type="text"
                bind:value={prompt}
                bind:this={inputElement}
                on:click={handleInputClick}
                placeholder={placeholder()}
                title="Enter a term. Hotkey: /"
                disabled={loading}
                aria-label="Enter a term. Hotkey: /"
        />
        <button type="submit" disabled={loading || !prompt}>
            {loading ? 'Please wait' : 'Submit'}
        </button>
    </div>
</form>

<style>
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
</style>
