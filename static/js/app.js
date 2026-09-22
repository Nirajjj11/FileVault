function confirmDelete(fileId, fileName) {

      const confirmed = confirm(
            `Are you sure you want to delete "${fileName}" ?\n\nThis action cannot be undone.`
      );

      if (!confirmed) {
            return;
      }

      const form = document.createElement("form");

      form.method = "POST";
      form.action = `/ storage / file / ${fileId} /delete/`;

      const csrfToken = document.querySelector(
            "[name=csrfmiddlewaretoken]"
      ).value;

      const csrfInput = document.createElement("input");

      csrfInput.type = "hidden";
      csrfInput.name = "csrfmiddlewaretoken";
      csrfInput.value = csrfToken;

      form.appendChild(csrfInput);

      document.body.appendChild(form);

      form.submit();
}