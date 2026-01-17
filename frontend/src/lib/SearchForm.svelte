<script>
    import {isValidYoutubeUrl, isYoutubePrompt} from "./utils.js";

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
     * Callback function to handle form submission.
     */
    export let onsubmit = undefined;

    /**
     * Reference to the input element in the DOM.
     */
    let inputElement;

    /**
     * Boolean flag indicating whether the input element is currently focused.
     */
    let isInputFocused = false;

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
            case 'YOUTUBE_EN':
                return 'https://youtu.be/j6PbonHsqW0?si=czYETvD9kJd-EWbi'
            case 'YOUTUBE_DE':
                return 'https://youtu.be/j6PbonHsqW0?si=czYETvD9kJd-EWbi'
        }
        return '';
    }

    /**
     * Returns the description for the current search type.
     */
    function description() {
        switch (type) {
            case 'DICTIONARY_EN':
                return 'A dictionary of the English language.';
            case 'ENCYCLOPEDIA_EN':
                return 'An encyclopedia answering in English language.';
            case 'ENCYCLOPEDIA_DE':
                return 'An encyclopedia answering in German language.';
            case 'YOUTUBE_EN':
                return 'A YouTube curator in English language.';
            case 'YOUTUBE_DE':
                return 'A YouTube curator in German language.';
        }
        return '';
    }

    /**
     * Checks if the current input is valid based on the selected type.
     */
    function isValidInput() {
        if (!prompt) {
            return false;
        }

        // YouTube types require URL starting with "https://youtu"
        if (isYoutubePrompt(type)) {
            return isValidYoutubeUrl(prompt);
        }

        return true;
    }

    /**
     * Returns validation error message if input is invalid.
     */
    function getValidationError() {
        if (!prompt) {
            return '';
        }

        if (isYoutubePrompt(type) && !isValidYoutubeUrl(prompt)) {
            return 'Please enter a YouTube link starting with https://(www.)youtu';
        }

        return '';
    }

    /**
     * Focuses the input element and selects all its text.
     * @returns {boolean} Whether the input element was focused successfully.
     */
    export function focusInputElement() {
        if (isInputFocused) {
            return false;
        }
        inputElement?.focus();
        inputElement?.select();
        isInputFocused = true;
        return true;
    }

    function blurInputElement() {
        isInputFocused = false;
    }

    /**
     * Handles the form submission.
     */
    function handleSubmit() {
        if (isValidInput()) {
            onsubmit?.();
        }
    }
</script>

<div class="form-wrapper">
    <form on:submit|preventDefault={handleSubmit}>
        <div class="search-container">
            <select bind:value={type} on:change={focusInputElement} disabled={loading}
                    aria-label="search type selector">
                <option value="DICTIONARY_EN">English Dictionary</option>
                <option value="ENCYCLOPEDIA_EN">English Encyclopedia</option>
                <option value="ENCYCLOPEDIA_DE">German Encyclopedia</option>
                <option value="YOUTUBE_EN">English YouTube</option>
                <option value="YOUTUBE_DE">German YouTube</option>
            </select>
            <input
                    type="text"
                    bind:value={prompt}
                    bind:this={inputElement}
                    on:click={focusInputElement}
                    on:blur={blurInputElement}
                    placeholder="{placeholder()}"
                    title="Enter a term. Hotkey: /"
                    disabled={loading}
                    aria-label="Enter a term. Hotkey: /"
            />
            <button type="submit" disabled={loading || !isValidInput()}>
                Submit
            </button>
        </div>
        {#if !isValidInput()}
            <p class="error-message">{getValidationError()}</p>
        {/if}
    </form>
    <p class="description">{description()}</p>
</div>

<style>
    .form-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1rem;
        margin-top: 2rem;
    }

    form {
        width: 100%;
        max-width: 800px;
    }

    .search-container {
        display: flex;
        align-items: center;
        gap: 0;
        background: white;
        border: 3px solid #5dd5d5;
        border-radius: 2rem;
        padding: 0.75rem 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    select {
        padding: 0.75rem 1rem;
        font-size: 1rem;
        background-color: #e8e8e8;
        border: none;
        border-radius: 0.5rem;
        margin-right: 1rem;
        cursor: pointer;
        appearance: none;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23333' d='M6 9L1 4h10z'/%3E%3C/svg%3E");
        background-repeat: no-repeat;
        background-position: right 0.75rem center;
        padding-right: 2.5rem;
    }

    input {
        flex: 1;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        background-color: white;
        border: none;
        outline: none;
    }

    input::placeholder {
        color: #999;
    }

    button {
        padding: 0.75rem 2rem;
        font-size: 1rem;
        background-color: #10b981;
        color: white;
        border: none;
        border-radius: 0.5rem;
        cursor: pointer;
        font-weight: 500;
        white-space: nowrap;
    }

    button:hover:not(:disabled) {
        background-color: #059669;
    }

    button:disabled {
        background-color: #9ca3af;
        cursor: not-allowed;
    }

    .description {
        margin: 0;
        color: #6b7280;
        font-size: 0.95rem;
        text-align: center;
    }

    .error-message {
        margin: 0.5rem 0 0;
        color: #dc2626;
        font-size: 0.875rem;
        text-align: center;
    }

    @media (max-width: 768px) {
        .search-container {
            flex-direction: column;
            gap: 0.75rem;
            padding: 1rem;
        }

        select {
            width: 100%;
            margin-right: 0;
        }

        input {
            width: 100%;
        }

        button {
            width: 100%;
        }
    }

    @media (prefers-color-scheme: dark) {
        .search-container {
            background: #1a1a1a;
            border-color: #5dd5d5;
        }

        select {
            background-color: #2a2a2a;
            color: rgba(255, 255, 255, 0.87);
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23fff' d='M6 9L1 4h10z'/%3E%3C/svg%3E");
        }

        input {
            background-color: #1a1a1a;
            color: rgba(255, 255, 255, 0.87);
        }

        input::placeholder {
            color: #666;
        }

        .description {
            color: #9ca3af;
        }

        .error-message {
            color: #ef4444;
        }
    }
</style>
