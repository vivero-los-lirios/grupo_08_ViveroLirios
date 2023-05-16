let menu = document.getElementById("menu__celular");
let nav = document.getElementById("menu__icono");
let hamburguesa = document.getElementById("menu-hamburguesa");
let cruz = document.getElementById("menu-cruz");
let item = document.querySelectorAll(".menu_li");

nav.addEventListener("click", (e) => {
  menu.classList.toggle("mostrar");
  hamburguesa.classList.toggle("close");
  cruz.classList.toggle("close");
});
item.forEach((i) => {
  i.addEventListener("click", (e) => {
    menu.classList.toggle("mostrar");
    hamburguesa.classList.toggle('close');
    cruz.classList.toggle('close');
  });
});

/* Funciones para cargar las provincias en el formulario */
let opcProvicia = document.getElementById("provincia");
let opcCiudad = document.getElementById("ciudad");

/*Funcion para buscar todas las provincias*/
let fetchProvicias = () => {
  return fetch('https://apis.datos.gob.ar/georef/api/provincias')
    .then(response => response.json())
    .catch(error => console.log(`Error al buscar las provincias. ${error}`));
}
/* Configuracion para que el selector de provincia se cargue cuando la pagina es lista*/
window.onload = async function (event) {
  
  event.preventDefault();
  console.log("evento click de provincia");
  const listaProvincias = await fetchProvicias();/*invoco a la fc para cargar las provincias*/
  /*Creo un string con el html para agregar todas provincias*/
  if (listaProvincias) {
    for (let i = 0; i < listaProvincias.cantidad; i++) {

      let newOption = document.createElement("option");
      newOption.text = `${listaProvincias.provincias[i].nombre}`;
      opcProvicia.add(newOption);
    }
    
  }
}


/* Funcion para traer las ciudades le la provincia seleccionada*/
let fetchCiudades = (buscarProv) => {
  return fetch(buscarProv)
  .then(response => response.json())
  .catch(error=>console.log(error));
}

/* Funciones para cargar las ciudades de la provincia seleccionada*/
opcProvicia.addEventListener('change', async function(event){
  event.preventDefault();
  
  let provinciaSeleccionada = opcProvicia.options[opcProvicia.selectedIndex].value;
  let BuscarProvincia = `https://apis.datos.gob.ar/georef/api/localidades?provincia=${provinciaSeleccionada}`;
  const listaCiudades = await fetchCiudades(BuscarProvincia);
  
  let delOpc = document.querySelector('#ciudad option');
  if(delOpc){
    delOpc.remove();
  } 
  
  if (listaCiudades) {
    for (let i = 0; i < listaCiudades.cantidad; i++) {

      let newOption = document.createElement("option");
      newOption.text = `${listaCiudades.localidades[i].nombre}`;
      opcCiudad.add(newOption);
    }
    
  }
})

