/** given data about a cupcake, generate html */

function generateCupcakeHTML(cupcake) {
    return `
      <div>
        <li>
          ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
          <button class="delete-cupcake btn-sm bun-danger" data-id="${cupcake.id}">Delete</button>
        <br>
        <img class="Cupcake-img" src="${cupcake.image}" alt="(no image provided)">
        </li>
      </div>
    `;
  }

/* handle add form submission to let api know and updates list on page */
$('#new-cupcake-form').on("submit", async function (evt) {
    evt.preventDefault()

    let flavor = $("#form-flavor").val();
    let size = $("#form-size").val();
    let rating = $("#form-rating").val();
    let image = $("#form-image").val();

    const newCupcakeResp = await axios.post(`/api/cupcakes`, {
        flavor,
        size,
        rating,
        image
    });

    let newCupcake = generateCupcakeHTML(newCupcakeResp.data.cupcake);
    $("#cupcakes-list").append(newCupcake);
    $("#new-cupcake-form").trigger("reset");

});

/** handle clicking delete: delete cupcake */
$("#cupcakes-list").on("click", ".delete-cupcake", async function (evt) {
    evt.preventDefault();

    const id = $(this).data('id');
    await axios.delete(`/api/cupcakes/${id}`)
    $(this).parent().remove()
  });
  