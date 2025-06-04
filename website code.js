// Initialize tooltips
const tooltipTriggerList = document.querySelectorAll(
  '[data-bs-toggle="tooltip"]'
);
tooltipTriggerList.forEach((el) => new bootstrap.Tooltip(el));

//feedback forms
let form = document.querySelector("#feedback");

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const form = document.querySelector("#feedback");
  const email = form.querySelector("#email");
  const name = form.querySelector("#name");
  const feedback = form.querySelector("#feedbacktext");

  console.log(email.value, name.value, feedback.value);

  const webhookURL =
    "https://discord.com/api/webhooks/1379688580699521175/NeAH5oqHPAN2uTbD2tdLydE90PRsLh4GYtAeEta50CSyKVWqAmwpiVgzacNqOr_yYHBI";
  fetch(webhookURL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      content: `## NEW FEEDBACK\ncontact:${email.value}\nfrom: ${name.value}\nFeedback:\n\`\`\`${feedback.value}\`\`\``,
    }),
  })
    .then(() => alert("Feedback sent!"))
    .catch((err) => alert("Error sending feedback."));
});
//
