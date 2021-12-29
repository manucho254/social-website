function toggleReplyButton(parent_id) {
    const commentForm = document.getElementById(parent_id);

    if (commentForm.classList.contains("d-none")) {
        commentForm.classList.remove("d-none");
    } else {
        commentForm.classList.add("d-none");
    }
}