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
  document.querySelector('#single-email-view').style.display = 'none';

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
  document.querySelector('#single-email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view-header').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetchMailbox(mailbox)
    .then(emails => displayEmails(emails));
}

function load_email(emailId) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  const singleEmailView = document.querySelector('#single-email-view');
  singleEmailView.style.display = 'block';
  singleEmailView.innerHTML = '';

  fetchEmailById(emailId)
    .then(email => displaySingleEmail(email))
    .catch(error => console.error(error));
}

function createButton(text, onClick) {
  const button = document.createElement('button');
  button.className = 'btn btn-sm btn-outline-primary';
  button.innerHTML = text;
  button.onclick = onClick;
  return button;
}

function displayEmails(emails) {
  const emailsTable = document.getElementById('emails-table-body');
  emailsTable.innerHTML = '';

  emails.forEach(email => {

    const emailRow = document.createElement('tr');
    emailRow.id = email.id;
    emailRow.style.background = email.read ? 'white' : 'lightgrey';
    emailRow.onclick = () => load_email(email.id);

    const from = document.createElement('td');
    from.innerHTML = email.sender;
    const subject = document.createElement('td');
    subject.innerHTML = email.subject;
    const timestamp = document.createElement('td');
    timestamp.innerHTML = email.timestamp;

    emailRow.appendChild(from);
    emailRow.appendChild(subject);
    emailRow.appendChild(timestamp);
    emailsTable.appendChild(emailRow);
  });
}

function displaySingleEmail(email) {
  const singleEmailView = document.querySelector('#single-email-view');

  if (!email.read) {
    readEmail(email.id, true)
      .catch((error) => console.error(error));
  }
  const from = document.createElement('div');
  from.innerHTML = `<strong>From:</strong> ${email.sender}`;
  const to = document.createElement('div');
  to.innerHTML = `<strong>To:</strong> ${email.recipients}`;
  const subject = document.createElement('div');
  subject.innerHTML = `<strong>Subject:</strong> ${email.subject}`;
  const timestamp = document.createElement('div');
  timestamp.innerHTML = `<strong>Timestamp:</strong> ${email.timestamp}`;
  const replyButton = createButton('Reply', () => replyEmail(email));
  const archiveButton = createButton(email.archived ? 'Un-archive' : 'Archive', () => {
    archiveEmail(email.id, !email.archived)
      .then(() => load_email(email.id));
  });
  const body = document.createElement('div');
  body.innerHTML = email.body;

  singleEmailView.appendChild(from);
  singleEmailView.appendChild(to);
  singleEmailView.appendChild(subject);
  singleEmailView.appendChild(timestamp);
  singleEmailView.appendChild(replyButton);
  singleEmailView.appendChild(archiveButton);
  singleEmailView.appendChild(body);
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
    .catch(error => console.error(error));
}
