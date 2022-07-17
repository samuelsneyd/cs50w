document.addEventListener('DOMContentLoaded', () => {
  const getCookie = (name) => {
    if (!document.cookie) {
      return null;
    }

    const xsrfCookies = document.cookie.split(';')
      .map(c => c.trim())
      .filter(c => c.startsWith(name + '='));

    if (xsrfCookies.length === 0) {
      return null;
    }
    return decodeURIComponent(xsrfCookies[0].split('=')[1]);
  };

  const followButton = document.getElementById('follow-button');
  if (followButton) {
    followButton.onclick = () => {
      const csrfToken = getCookie('csrftoken');
      const options = {
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken },
        body: JSON.stringify({
          post: parseInt(followButton.dataset.id)
        })
      };
      fetch(`/follow/${followButton.dataset.id}`, options)
        .catch((e) => console.error(e));

      const followersCountElement = document.getElementById('followers-count');
      const [followersText, followersCount] = followersCountElement.innerText.split(' ');
      if (followButton.classList.contains('following')) {
        followButton.classList.remove('following');
        followButton.innerText = 'Follow';
        followersCountElement.innerText = `${followersText} ${parseInt(followersCount) - 1}`;
      } else {
        followButton.classList.add('following');
        followButton.innerText = 'Unfollow';
        followersCountElement.innerText = `${followersText} ${parseInt(followersCount) + 1}`;
      }
    };
  }

  const likeButtons = [...document.getElementsByClassName('likes-count')];
  if (likeButtons.length > 0) {
    likeButtons.forEach((likeButton) => {
      likeButton.onclick = () => {
        const csrfToken = getCookie('csrftoken');
        const options = {
          method: 'POST',
          headers: { 'X-CSRFToken': csrfToken },
          body: JSON.stringify({
            post: parseInt(likeButton.dataset.id)
          })
        };
        fetch(`/like/${likeButton.dataset.id}`, options)
          .catch((e) => console.error(e));

        const [heartIcon, likesCount, likesText] = likeButton.innerText.split(' ');
        if (likeButton.classList.contains('liked')) {
          likeButton.innerText = `${heartIcon} ${parseInt(likesCount) - 1} ${likesText}`;
          likeButton.classList.remove('liked');
        } else {
          likeButton.innerText = `${heartIcon} ${parseInt(likesCount) + 1} ${likesText}`;
          likeButton.classList.add('liked');
        }
      };
    });
  }

  const editButtons = [...document.getElementsByClassName('post-edit-button')];
  if (editButtons.length > 0) {
    editButtons.forEach((editButton) => {
      editButton.onclick = () => {
        const postId = editButton.dataset.id;
        const editDiv = document.getElementById(`edit-post-${postId}`);
        const postText = document.getElementById(`post-text-${postId}`);
        editDiv.style.display = 'block';
        postText.style.display = 'none';
      };
    });
  }

  const saveEditButtons = [...document.getElementsByClassName('edit-submit-button')];
  if (saveEditButtons.length > 0) {
    saveEditButtons.forEach((saveButton) => {
      saveButton.onclick = () => {
        const postId = saveButton.dataset.id;
        const editDiv = document.getElementById(`edit-post-${postId}`);
        const postText = document.getElementById(`post-text-${postId}`);
        const postTextArea = document.getElementById(`edit-post-textarea-${postId}`);

        postText.innerText = postTextArea.value;
        editDiv.style.display = 'none';
        postText.style.display = 'block';

        const csrfToken = getCookie('csrftoken');
        const options = {
          method: 'POST',
          headers: { 'X-CSRFToken': csrfToken },
          body: JSON.stringify({
            text: postTextArea.value
          })
        };
        fetch(`/edit-post/${postId}`, options)
          .catch((e) => console.error(e));
      };
    });
  }
});
