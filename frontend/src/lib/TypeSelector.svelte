<script>
    export let type;
    export let disabled = false;
    export let onChange;
</script>

<select bind:value={type} on:change={onChange} disabled={disabled}>
    <option value="DICTIONARY_EN">Dictionary English</option>
    <option value="ENCYCLOPEDIA_EN">Encyclopedia English</option>
    <option value="ENCYCLOPEDIA_DE">Encyclopedia German</option>
</select>

<style>
    select {
        padding: 0.5rem;
        font-size: 1rem;
        border: 1px solid #ccc;
        border-radius: 4px;
        margin-bottom: 1rem;
        width: max(250px, 33%);
    }

    @media (prefers-color-scheme: dark) {
        select {
            background-color: #1a1a1a;
            color: rgba(255, 255, 255, 0.87);
            border-color: #555;
        }
    }
</style>
