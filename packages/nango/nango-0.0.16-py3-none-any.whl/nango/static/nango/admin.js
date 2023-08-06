/* eslint-disable no-unused-vars, quotes */

/**
  // remove any validation errors/states/classes relating to a prior 'clean' result,
  // which is now obsolete
  document
    .querySelectorAll(
      `[data-message-for-form-id=${data.dataset.relatedFormId}]`
    )
    .forEach(element => element.remove());

  if (data.cleanedValue) {
    // update the form input to show the cleaned value as returned from django
    visibleInput.value = data.cleanedValue;
    visibleInput.dataset.nangoState = "clean";
    return;
  }
  if (data.validationErrors) {
    visibleInput.dataset.nangoState = "dirty";
    nangoShowValidationError(data.dataset.relatedFormId, data.validationErrors);
  }
}
**/

function nangoShowValidationError(inputId, validationErrors) {
  console.log(validationErrors);
  const div = document.createElement("div");
  const ul = document.createElement("ul");
  ul.classList.add("errorlist");
  const li = document.createElement("li");
  li.appendChild(document.createTextNode(`${validationErrors}`));
  ul.appendChild(li);
  div.appendChild(ul);
  div.dataset.messageForFormId = inputId;
  const input = document.getElementById(inputId);
  input.parentNode.insertBefore(div, input.nextSibling);
}
