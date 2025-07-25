<script>
  import { onMount } from 'svelte';
  let notes = [];
  let title = '';
  let content = '';

  async function fetchNotes() {
    const res = await fetch('http://localhost:8000/notes');
    notes = await res.json();
  }

  async function addNote() {
    await fetch('http://localhost:8000/notes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, content })
    });
    title = ''; content = '';
    await fetchNotes();
  }

  onMount(fetchNotes);
</script>

<main>
  <h1>OmniScribe</h1>
  <div>
    <input bind:value={title} placeholder="Title" />
    <textarea bind:value={content} placeholder="Markdown content"></textarea>
    <button on:click={addNote}>Add Note</button>
  </div>
  {#each notes as note}
    <div>
      <h2>{note.title}</h2>
      <p>{note.content}</p>
    </div>
  {/each}
</main>