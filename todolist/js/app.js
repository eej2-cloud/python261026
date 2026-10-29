"use strict";

const STORAGE_KEY = "todolist.items";
const FILTERS = new Set(["all", "active", "completed"]);

const form = document.querySelector("#todo-form");
const input = document.querySelector("#todo-input");
const list = document.querySelector("#todo-list");
const emptyState = document.querySelector("#empty-state");
const taskCount = document.querySelector("#task-count");
const notice = document.querySelector("#storage-notice");
const announcement = document.querySelector("#list-announcement");
const filterButtons = [...document.querySelectorAll("[data-filter]")];

let items = [];
let currentFilter = "all";
let storageReady = false;

function isValidItems(value) {
  if (!Array.isArray(value)) {
    return false;
  }

  const ids = new Set();
  return value.every((item) => {
    if (
      item === null ||
      typeof item !== "object" ||
      typeof item.id !== "string" ||
      item.id.length === 0 ||
      typeof item.text !== "string" ||
      item.text.trim().length === 0 ||
      typeof item.completed !== "boolean" ||
      typeof item.createdAt !== "string" ||
      Number.isNaN(Date.parse(item.createdAt)) ||
      ids.has(item.id)
    ) {
      return false;
    }

    ids.add(item.id);
    return true;
  });
}

function setNotice(message) {
  notice.textContent = message;
  notice.hidden = message.length === 0;
}

function setStorageReady(ready) {
  storageReady = ready;
  form.querySelectorAll("input, button").forEach((control) => {
    control.disabled = !ready;
  });
  list.querySelectorAll("input, button").forEach((control) => {
    control.disabled = !ready;
  });
}

function loadItems() {
  try {
    const storedValue = window.localStorage.getItem(STORAGE_KEY);
    if (storedValue === null) {
      items = [];
      setStorageReady(true);
      setNotice("");
      return;
    }

    const parsedValue = JSON.parse(storedValue);
    if (!isValidItems(parsedValue)) {
      throw new Error("저장된 할 일 데이터의 형식이 올바르지 않습니다.");
    }

    items = parsedValue;
    setStorageReady(true);
    setNotice("");
  } catch (error) {
    items = [];
    setStorageReady(false);
    setNotice(
      error instanceof SyntaxError
        ? "저장된 목록을 읽을 수 없습니다. 기존 데이터는 보존했으며, 데이터를 덮어쓰지 않도록 편집 기능을 잠갔습니다."
        : `저장소를 사용할 수 없습니다. 기존 데이터는 보존했으며 편집 기능을 잠갔습니다. (${error.message})`,
    );
  }
}

function saveItems(nextItems) {
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(nextItems));
    items = nextItems;
    render();
    return true;
  } catch (error) {
    setStorageReady(false);
    setNotice(`목록을 저장하지 못했습니다. 변경 사항은 적용되지 않았습니다. (${error.message})`);
    render();
    return false;
  }
}

function createId() {
  if (typeof window.crypto?.randomUUID === "function") {
    return window.crypto.randomUUID();
  }
  return `${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}`;
}

function getVisibleItems() {
  if (currentFilter === "active") {
    return items.filter((item) => !item.completed);
  }
  if (currentFilter === "completed") {
    return items.filter((item) => item.completed);
  }
  return items;
}

function createTodoElement(item) {
  const listItem = document.createElement("li");
  listItem.className = `todo-item${item.completed ? " is-completed" : ""}`;

  const checkbox = document.createElement("input");
  checkbox.className = "todo-toggle";
  checkbox.type = "checkbox";
  checkbox.checked = item.completed;
  checkbox.disabled = !storageReady;
  checkbox.setAttribute("aria-label", `${item.text} 완료`);
  checkbox.addEventListener("change", () => {
    const nextItems = items.map((currentItem) =>
      currentItem.id === item.id
        ? { ...currentItem, completed: checkbox.checked }
        : currentItem,
    );
    if (saveItems(nextItems)) {
      announcement.textContent = checkbox.checked
        ? `${item.text} 완료 처리했습니다.`
        : `${item.text} 완료를 취소했습니다.`;
    }
  });

  const text = document.createElement("span");
  text.className = "todo-text";
  text.textContent = item.text;

  const deleteButton = document.createElement("button");
  deleteButton.className = "delete-button";
  deleteButton.type = "button";
  deleteButton.disabled = !storageReady;
  deleteButton.setAttribute("aria-label", `${item.text} 삭제`);
  deleteButton.textContent = "×";
  deleteButton.addEventListener("click", () => {
    if (saveItems(items.filter((currentItem) => currentItem.id !== item.id))) {
      announcement.textContent = `${item.text} 삭제했습니다.`;
    }
  });

  listItem.append(checkbox, text, deleteButton);
  return listItem;
}

function render() {
  const visibleItems = getVisibleItems();
  list.replaceChildren(...visibleItems.map(createTodoElement));
  taskCount.textContent = String(items.length);
  taskCount.setAttribute("aria-label", `전체 할 일 ${items.length}개`);
  emptyState.hidden = visibleItems.length > 0;

  if (items.length === 0) {
    emptyState.querySelector(".empty-title").textContent = "아직 할 일이 없어요";
    emptyState.querySelector(".empty-copy").textContent = storageReady
      ? "새로운 할 일을 추가해 보세요."
      : "저장된 목록을 복구한 뒤 다시 이용할 수 있습니다.";
  } else if (visibleItems.length === 0) {
    emptyState.querySelector(".empty-title").textContent =
      currentFilter === "active" ? "진행 중인 할 일이 없어요" : "완료한 할 일이 없어요";
    emptyState.querySelector(".empty-copy").textContent = "다른 필터를 선택해 목록을 확인하세요.";
  }

  filterButtons.forEach((button) => {
    const selected = button.dataset.filter === currentFilter;
    button.classList.toggle("is-active", selected);
    button.setAttribute("aria-pressed", String(selected));
  });
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  if (!storageReady) {
    return;
  }

  const text = input.value.trim();
  if (!text) {
    input.focus();
    return;
  }

  const nextItems = [
    ...items,
    {
      id: createId(),
      text,
      completed: false,
      createdAt: new Date().toISOString(),
    },
  ];

  if (saveItems(nextItems)) {
    input.value = "";
    input.focus();
    announcement.textContent = `${text} 추가했습니다.`;
  }
});

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const filter = button.dataset.filter;
    if (!FILTERS.has(filter)) {
      return;
    }
    currentFilter = filter;
    render();
  });
});

loadItems();
render();
