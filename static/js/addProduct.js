const productForm = document.getElementById("product-form");
const productAlert = document.getElementById("product-alert");

// Función para generar productos ficticios y agregarlos al localStorage
function generateDummyProducts(numProducts) {
  const dummyProducts = [];
  const categories = ["Category 1", "Category 2", "Category 3", "Category 4"];

  for (let i = 1; i <= numProducts; i++) {
    const newProduct = {
      id: `ABC${i}`,
      name: `Product ${i}`,
      desc: `Description of Product ${i}`,
      ubi: `Location ${i}`,
      cant: Math.floor(Math.random() * 10) + 1, // Random quantity between 1 and 10
      pdf: "",
      categ: categories[Math.floor(Math.random() * categories.length)] // Random category from the array
    };
    dummyProducts.push(newProduct);
  }
  setProductsInLocalStorage(dummyProducts);
}

// Llamar a la función para generar 100 productos ficticios
generateDummyProducts(50);

productForm.addEventListener("submit", (e) => {
  e.preventDefault();

  const productId = document.getElementById("product-id").value.trim();
  const productName = document.getElementById("product-name").value.trim();
  const productDesc = document.getElementById("product-desc").value.trim();
  const productUbi = document.getElementById("product-ubi").value.trim();
  const productCant = parseInt(document.getElementById("product-cant").value, 10);
  const productPdf = document.getElementById("product-pdf").files[0];
  const productCateg = document.getElementById("product-categ").value;

  const newProduct = {
    id: productId,
    name: productName,
    desc: productDesc,
    ubi: productUbi,
    cant: productCant,
    pdf: productPdf ? productPdf.name : "",
    categ: productCateg,
  };

  const products = getProductsFromLocalStorage();

  const productExists = products.some((product) => product.id === productId);

  if (productExists) {
    productAlert.classList.remove("d-none");
    productAlert.textContent = "El producto con este número de serie ya existe.";
    return;
  }

  productAlert.classList.add("d-none");

  // GUARDAR EN LOCAL STORAGE
  products.push(newProduct);
  setProductsInLocalStorage(products);


  productForm.reset();


  window.location.href = "/inventario/editor";
});


function getProductsFromLocalStorage() {
  const productsJSON = localStorage.getItem("products");
  return productsJSON ? JSON.parse(productsJSON) : [];
}

function setProductsInLocalStorage(products) {
  localStorage.setItem("products", JSON.stringify(products));
}
