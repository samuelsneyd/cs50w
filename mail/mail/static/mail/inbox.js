document.addEventListener('DOMContentLoaded', function () {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Add event listener to submit button
  document.querySelector('#compose-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;
    sendEmail(recipients, subject, body)
      .then(() => load_mailbox('sent'));
  });
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetchMailbox(mailbox)
    .then(emails => displayEmails(emails));
}

function displayEmails(emails) {
  const emailsView = document.getElementById('emails-view');

  emails.forEach(email => {
    const emailElement = document.createElement('div');
    emailElement.className = 'col-md-12';

    const rowColumn = document.createElement('div');
    rowColumn.className = 'col-md-8';
    rowColumn.innerHTML = `From: ${email.sender} | Subject: ${email.subject} | Timestamp: ${email.timestamp}`;

    const rowControls = document.createElement('div');
    rowControls.className = 'col-md-4';

    const viewButton = document.createElement('button');
    viewButton.innerHTML = 'View';
    viewButton.onclick = () => {};

    const replyButton = document.createElement('button');
    replyButton.innerHTML = 'Reply';
    replyButton.onclick = () => replyEmail(email);

    const archiveButton = document.createElement('button');
    archiveButton.innerHTML = email.archived ? 'Un-archive' : 'Archive';
    archiveButton.onclick = () => {
      archiveEmail(email.id, !email.archived).then(() => {
        archiveButton.parentElement.parentElement.remove();
      })
    };

    rowControls.append(viewButton);
    rowControls.append(replyButton);
    rowControls.append(archiveButton);

    emailElement.append(rowColumn);
    emailElement.append(rowControls);

    emailsView.append(emailElement);
  });
}

function viewEmail(email) {
  // TODO
}

function replyEmail(email) {
  const { sender, subject, timestamp, body } = email;
  compose_email();
  document.querySelector('#compose-recipients').value = sender;
  document.querySelector('#compose-subject').value = `Re: ${subject}`;
  document.querySelector('#compose-body').value = `\n\nOn ${timestamp} ${sender} wrote:\n\n${body}`;
}

function fetchMailbox(mailbox) {
  return fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .catch(error => console.error(error));
}

function fetchEmailById(emailId) {
  return fetch(`/emails/${emailId}`)
    .then(response => response.json())
    .catch(error => console.error(error));
}

function sendEmail(recipients, subject, body) {
  return fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients,
      subject,
      body
    })
  })
    .then(response => response.json())
    .catch(error => console.error(error));
}

function archiveEmail(emailId, isArchived) {
  return fetch(`/emails/${emailId}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: isArchived
    })
  })
    .catch(error => console.error(error));
}

function readEmail(emailId, isRead) {
  return fetch(`/emails/${emailId}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: isRead
    })
  })
    .then(response => response.json())
    .catch(error => console.error(error));
}
