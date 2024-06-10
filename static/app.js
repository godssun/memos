const form = document.querySelector("#memo-form");
form.addEventListener("submit", handleSubmit);

let currentSortBy = "createAt";
let currentOrder = "ASC";

function setSort(sortBy, order) {
  currentSortBy = sortBy;
  currentOrder = order;
  readMemo();
}

async function editMemo(event) {
  const id = event.target.dataset.id;
  const editInput = prompt("수정할 값을 입력하세요!!");
  if (!editInput) return;

  const res = await fetch(`/memos/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: parseInt(id), // id를 정수로 변환
      content: editInput,
    }),
  });

  if (res.ok) {
    readMemo();
  } else {
    console.error("Failed to edit memo", await res.text());
  }
}

async function deleteMemo(event) {
  const id = event.target.dataset.id;
  const res = await fetch(`/memos/${id}`, {
    method: "DELETE",
  });

  if (res.ok) {
    readMemo();
  } else {
    console.error("Failed to delete memo", await res.text());
  }
}

function displayMemo(memo) {
  const ul = document.querySelector(".memo-ul");
  const li = document.createElement("li");
  const editBtn = document.createElement("button");
  const delBtn = document.createElement("button");

  editBtn.innerText = "수정";
  editBtn.addEventListener("click", editMemo);
  editBtn.dataset.id = memo.id;

  delBtn.innerText = "삭제";
  delBtn.addEventListener("click", deleteMemo);
  delBtn.dataset.id = memo.id;

  li.innerText = `${memo.content}`;

  ul.appendChild(li);
  li.appendChild(editBtn);
  li.appendChild(delBtn);
}

async function readMemo() {
  const res = await fetch(`/memos?sortedBy=${currentSortBy}&order=${currentOrder}`);
  const jsonRes = await res.json();
  const ul = document.querySelector(".memo-ul");
  ul.innerText = "";
  jsonRes.forEach(displayMemo);
}

async function createMemo(value) {
  const res = await fetch("/memos", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: new Date().getTime(),
      content: value,
      title: value, // Title도 content와 같은 값으로 임시 설정
      createAt: new Date().toISOString(), // 현재 시간을 createAt으로 설정
    }),
  });

  if (res.ok) {
    readMemo();
  } else {
    console.error("Failed to create memo", await res.text());
  }
}

function handleSubmit(event) {
  event.preventDefault();
  const input = document.querySelector("#memo-input");
  createMemo(input.value);
  input.value = "";
}

readMemo();
