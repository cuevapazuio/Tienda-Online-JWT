const API = "http://127.0.0.1:8000";

let token = localStorage.getItem("token") || "";
let username = localStorage.getItem("username") || "";


const authSection =
    document.getElementById("auth-section");

const appSection =
    document.getElementById("app-section");

const authMensaje =
    document.getElementById("auth-mensaje");

const estado =
    document.getElementById("estado");

const productos =
    document.getElementById("productos");

const usuarioActivo =
    document.getElementById("usuario-activo");

const productoForm =
    document.getElementById("producto-form");

const formTitle =
    document.getElementById("form-title");

const cancelarBtn =
    document.getElementById("cancelar-btn");


async function peticion(
    ruta,
    metodo = "GET",
    datos = null
) {
    const headers = {
        "Content-Type": "application/json"
    };

    if (token) {
        headers.Authorization = `Bearer ${token}`;
    }

    const opciones = {
        method: metodo,
        headers: headers
    };

    if (datos !== null) {
        opciones.body = JSON.stringify(datos);
    }

    const respuesta = await fetch(
        `${API}${ruta}`,
        opciones
    );

    if (respuesta.status === 204) {
        return null;
    }

    const contenido = await respuesta.json();

    if (!respuesta.ok) {

        let mensaje = contenido.detail;

        if (typeof mensaje !== "string") {
            mensaje = "Solicitud no válida";
        }

        throw new Error(mensaje);
    }

    return contenido;
}


function mostrarAplicacion() {

    authSection.classList.add("oculto");
    appSection.classList.remove("oculto");

    usuarioActivo.textContent =
        `Usuario: ${username}`;

    cargarProductos();
}


function cerrarSesion() {

    token = "";
    username = "";

    localStorage.removeItem("token");
    localStorage.removeItem("username");

    appSection.classList.add("oculto");
    authSection.classList.remove("oculto");

    authMensaje.textContent =
        "Sesión cerrada";
}


/* =========================
   REGISTRO
========================= */

document
    .getElementById("register-form")
    .addEventListener(
        "submit",
        async function (evento) {

            evento.preventDefault();

            const datos = {
                username:
                    document.getElementById(
                        "register-username"
                    ).value,

                email:
                    document.getElementById(
                        "register-email"
                    ).value,

                password:
                    document.getElementById(
                        "register-password"
                    ).value
            };

            try {

                await peticion(
                    "/auth/register",
                    "POST",
                    datos
                );

                authMensaje.textContent =
                    "Usuario registrado correctamente";

                authMensaje.className =
                    "mensaje exito";

                document.getElementById(
                    "login-username"
                ).value = datos.username;

                this.reset();

            } catch (error) {

                authMensaje.textContent =
                    error.message;

                authMensaje.className =
                    "mensaje error";
            }
        }
    );


/* =========================
   LOGIN
========================= */

document
    .getElementById("login-form")
    .addEventListener(
        "submit",
        async function (evento) {

            evento.preventDefault();

            const usuario =
                document.getElementById(
                    "login-username"
                ).value;

            const password =
                document.getElementById(
                    "login-password"
                ).value;

            try {

                const respuesta =
                    await peticion(
                        "/auth/login",
                        "POST",
                        {
                            username: usuario,
                            password: password
                        }
                    );

                token =
                    respuesta.access_token;

                username =
                    usuario;

                localStorage.setItem(
                    "token",
                    token
                );

                localStorage.setItem(
                    "username",
                    username
                );

                mostrarAplicacion();

            } catch (error) {

                authMensaje.textContent =
                    error.message;

                authMensaje.className =
                    "mensaje error";
            }
        }
    );


/* =========================
   PRODUCTOS
========================= */

async function cargarProductos() {

    try {

        const lista =
            await peticion(
                "/productos/"
            );

        mostrarProductos(lista);

        estado.textContent =
            `${lista.length} productos`;

    } catch (error) {

        estado.textContent =
            error.message;

        estado.className =
            "mensaje error";

        if (
            error.message.includes(
                "Autenticacion"
            ) ||
            error.message.includes(
                "Token"
            )
        ) {
            cerrarSesion();
        }
    }
}


function mostrarProductos(lista) {

    productos.replaceChildren();

    if (lista.length === 0) {

        const mensaje =
            document.createElement("p");

        mensaje.textContent =
            "No existen productos.";

        productos.append(mensaje);

        return;
    }

    lista.forEach(function (producto) {

        const tarjeta =
            document.createElement("article");

        tarjeta.className =
            "producto";


        const nombre =
            document.createElement("h3");

        nombre.textContent =
            producto.nombre;


        const descripcion =
            document.createElement("p");

        descripcion.className =
            "descripcion";

        descripcion.textContent =
            producto.descripcion || "Sin descripción";


        const precio =
            document.createElement("p");

        precio.className =
            "precio";

        precio.textContent =
            `$${producto.precio.toFixed(2)}`;


        const stock =
            document.createElement("p");

        stock.className =
            "stock";

        stock.textContent =
            `Stock: ${producto.stock}`;


        const botones =
            document.createElement("div");

        botones.className =
            "botones";


        const editar =
            document.createElement("button");

        editar.textContent =
            "Editar";

        editar.addEventListener(
            "click",
            function () {
                editarProducto(producto);
            }
        );


        const eliminar =
            document.createElement("button");

        eliminar.textContent =
            "Eliminar";

        eliminar.className =
            "peligro";

        eliminar.addEventListener(
            "click",
            function () {
                eliminarProducto(
                    producto.id
                );
            }
        );


        botones.append(
            editar,
            eliminar
        );

        tarjeta.append(
            nombre,
            descripcion,
            precio,
            stock,
            botones
        );

        productos.append(tarjeta);
    });
}


/* =========================
   GUARDAR / ACTUALIZAR
========================= */

productoForm.addEventListener(
    "submit",
    async function (evento) {

        evento.preventDefault();

        const id =
            document.getElementById(
                "producto-id"
            ).value;

        const datos = {

            nombre:
                document.getElementById(
                    "nombre"
                ).value,

            descripcion:
                document.getElementById(
                    "descripcion"
                ).value,

            precio:
                Number(
                    document.getElementById(
                        "precio"
                    ).value
                ),

            stock:
                Number(
                    document.getElementById(
                        "stock"
                    ).value
                )
        };

        try {

            if (id) {

                await peticion(
                    `/productos/${id}`,
                    "PUT",
                    datos
                );

            } else {

                await peticion(
                    "/productos/",
                    "POST",
                    datos
                );
            }

            limpiarFormulario();

            cargarProductos();

        } catch (error) {

            estado.textContent =
                error.message;

            estado.className =
                "mensaje error";
        }
    }
);


function editarProducto(producto) {

    document.getElementById(
        "producto-id"
    ).value = producto.id;

    document.getElementById(
        "nombre"
    ).value = producto.nombre;

    document.getElementById(
        "descripcion"
    ).value =
        producto.descripcion || "";

    document.getElementById(
        "precio"
    ).value = producto.precio;

    document.getElementById(
        "stock"
    ).value = producto.stock;

    formTitle.textContent =
        "Editar producto";

    cancelarBtn.classList.remove(
        "oculto"
    );

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}


function limpiarFormulario() {

    productoForm.reset();

    document.getElementById(
        "producto-id"
    ).value = "";

    formTitle.textContent =
        "Nuevo producto";

    cancelarBtn.classList.add(
        "oculto"
    );
}


/* =========================
   ELIMINAR
========================= */

async function eliminarProducto(id) {

    const confirmar =
        confirm(
            "¿Eliminar este producto?"
        );

    if (!confirmar) {
        return;
    }

    try {

        await peticion(
            `/productos/${id}`,
            "DELETE"
        );

        cargarProductos();

    } catch (error) {

        estado.textContent =
            error.message;
    }
}


/* =========================
   EVENTOS
========================= */

cancelarBtn.addEventListener(
    "click",
    limpiarFormulario
);


document
    .getElementById("actualizar-btn")
    .addEventListener(
        "click",
        cargarProductos
    );


document
    .getElementById("logout-btn")
    .addEventListener(
        "click",
        cerrarSesion
    );


/* =========================
   INICIO
========================= */

if (token) {
    mostrarAplicacion();
}