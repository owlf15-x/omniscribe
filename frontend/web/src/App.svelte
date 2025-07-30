<script lang="ts">
  import "./App.css";
  import { onMount } from "svelte";
  import { marked } from "marked";

  interface Note {
    id: number;
    title: string;
    content: string;
  }

  let notes: Note[] = [];
  let title = "";
  let content = "";

  let showModal = false;
  let currentNote: Note | null = null;
  let isEditing = false;
  let editTitle = "";
  let editContent = "";

  marked.setOptions({ gfm: true, breaks: true });

  async function fetchNotes() {
    const res = await fetch("http://localhost:8000/notes");
    notes = await res.json();
  }

  async function addNote() {
    await fetch("http://localhost:8000/notes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, content }),
    });
    title = "";
    content = "";
    await fetchNotes();
  }

  async function updateNote() {
    if (!currentNote) return;
    await fetch(`http://localhost:8000/notes/${currentNote.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: editTitle, content: editContent }),
    });
    isEditing = false;
    await fetchNotes();
    const updatedNote = notes.find((n) => n.id === currentNote?.id);
    if (updatedNote) currentNote = updatedNote;
  }

  function openModal(note: Note) {
    currentNote = note;
    isEditing = false;
    showModal = true;
  }

  function closeModal() {
    showModal = false;
    currentNote = null;
    isEditing = false;
    editTitle = "";
    editContent = "";
  }

  function startEdit() {
    if (!currentNote) return;
    editTitle = currentNote.title;
    editContent = currentNote.content;
    isEditing = true;
  }

  async function copyContent(textToCopy: string) {
    try {
      await navigator.clipboard.writeText(textToCopy);
      alert("Скопировано, братишка! 🎉");
    } catch (err) {
      console.error("Ошибка копирования:", err);
      alert("Пиздец, не скопировалось :(");
    }
  }

  onMount(fetchNotes);
</script>

<main>
  <h1>OmniScribe</h1>
  <p class="subtitle">
    Всякие интересные заметки. И... не очень интересные заметки.
  </p>
  <div class="input-group">
    <input bind:value={title} placeholder="Титлэ" />
    <textarea
      bind:value={content}
      placeholder="Контент (Markdown поддерживается)"
    ></textarea>
    <button on:click={addNote}>Добавить</button>
  </div>

  <div class="notes-list">
    {#each notes as note}
      <div class="note-preview">
        <span class="note-title">{note.title}</span>
        <div class="note-actions">
          <button class="btn-small" on:click={() => openModal(note)}
            >Показать</button
          >
          <button class="btn-small" on:click={() => copyContent(note.content)}
            >Копировать</button
          >
          <button
            class="btn-small"
            on:click={() => {
              openModal(note);
              startEdit();
            }}>Редактировать</button
          >
        </div>
      </div>
    {/each}
  </div>
</main>

{#if showModal && currentNote}
  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <!-- svelte-ignore a11y-no-static-element-interactions -->
  <div class="modal-overlay" on:click={closeModal}>
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <!-- svelte-ignore a11y-no-static-element-interactions -->
    <div class="modal-content" on:click|stopPropagation>
      {#if isEditing}
        <h2>Редактирование заметки</h2>
        <input bind:value={editTitle} placeholder="Заголовок" />
        <textarea bind:value={editContent} placeholder="Содержимое (Markdown)"
        ></textarea>
        <div class="modal-actions">
          <button on:click={updateNote}>Сохранить</button>
          <button on:click={() => (isEditing = false)}>Отмена</button>
        </div>
      {:else}
        <h2>{currentNote.title}</h2>
        <div class="modal-actions">
          <button on:click={() => copyContent(currentNote.content)}
            >Копировать</button
          >
          <button on:click={startEdit}>Редактировать</button>
          <button on:click={closeModal}>Закрыть</button>
        </div>
        <div class="note-body">{@html marked(currentNote.content)}</div>
      {/if}
    </div>
  </div>
{/if}
