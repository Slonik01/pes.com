function like(cardId) {

    const likeCount = document.getElementById(`likes-count-${cardId}`);
    const likeButton = document.getElementById(`like-button-${cardId}`);
  
    fetch(`/likep/${cardId}`, { method: "POST" }).then((res) => res.json()).then((data) => {

        likeCount.innerHTML = `❤   ${data["likes"]}`;
        if (data["liked"] === true) {
          likeButton.className = "btn btn-danger";
        } else {
          likeButton.className = "btn btn-outline-danger";
        }

      })

      .catch((e) => alert("Could not like post."));
  }



function likepost(postId) {

    const likeCount = document.getElementById(`likes-count-${postId}`);
    const likeButton = document.getElementById(`like-button-${postId}`);
  
    fetch(`/liken/${postId}`, { method: "POST" }).then((res) => res.json()).then((data) => {

        likeCount.innerHTML = `❤   ${data["likes"]}`;
        if (data["liked"] === true) {
          likeButton.className = "btn btn-danger";
        } else {
          likeButton.className = "btn btn-outline-danger";
        }

      })

      .catch((e) => alert("Could not like post."));
  }