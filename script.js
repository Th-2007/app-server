// =====================================
// FILEBOX SERVER v1.0
// Control del panel web
// =====================================


let allFiles = [];



// ------------------------------
// ABRIR SELECTOR DE ARCHIVOS
// ------------------------------

function openUpload(){

    document
    .getElementById("fileInput")
    .click();

}




// ------------------------------
// SUBIR ARCHIVO
// ------------------------------

async function uploadFile(){


    let input =
    document.getElementById("fileInput");


    let file =
    input.files[0];


    if(!file)
    return;



    let data =
    new FormData();


    data.append(
        "file",
        file
    );



    let res =
    await fetch(
        "/api/upload",
        {
            method:"POST",
            body:data
        }
    );



    let result =
    await res.json();



    alert(
        "Archivo subido: "
        + result.file
    );



    input.value="";


    loadFiles();

}




// ------------------------------
// CARGAR ARCHIVOS
// ------------------------------

async function loadFiles(){


    let res =
    await fetch(
        "/api/files"
    );


    allFiles =
    await res.json();



    renderFiles(
        allFiles
    );



    updateStats();

}



// ------------------------------
// MOSTRAR ARCHIVOS
// ------------------------------

function renderFiles(files){


    let list =
    document.getElementById(
        "fileList"
    );



    list.innerHTML="";



    if(files.length===0){


        list.innerHTML=
        `
        <tr>
        <td colspan="4">
        No hay archivos
        </td>
        </tr>
        `;

        return;

    }




    files.forEach(file=>{


        let row =
        document.createElement(
            "tr"
        );



        row.innerHTML=

        `

        <td>
        📄 ${file.name}
        </td>


        <td>
        ${formatSize(file.size)}
        </td>


        <td>
        ${file.date}
        </td>


        <td>


        <button
        class="action download"
        onclick="downloadFile('${file.path}')">

        ⬇

        </button>



        <button
        class="action rename"
        onclick="renameFile('${file.path}')">

        ✏

        </button>



        <button
        class="action delete"
        onclick="deleteFile('${file.path}')">

        🗑

        </button>


        </td>


        `;



        list.appendChild(row);


    });


}



// ------------------------------
// DESCARGAR
// ------------------------------

function downloadFile(path){


    window.location.href =
    "/api/download/"
    +
    encodeURIComponent(path);


}



// ------------------------------
// BORRAR
// ------------------------------

async function deleteFile(path){



    if(
    !confirm(
    "¿Eliminar archivo?"
    )
    )
    return;



    await fetch(
        "/api/delete",
        {

        method:"POST",

        headers:
        {
        "Content-Type":
        "application/json"
        },


        body:
        JSON.stringify({

            path:path

        })

        }
    );



    loadFiles();


}





// ------------------------------
// RENOMBRAR
// ------------------------------

async function renameFile(oldName){



    let nuevo =
    prompt(
    "Nuevo nombre:",
    oldName
    );



    if(!nuevo)
    return;



    await fetch(
    "/api/rename",
    {

    method:"POST",

    headers:
    {
    "Content-Type":
    "application/json"
    },


    body:
    JSON.stringify({

        old:oldName,

        new:nuevo

    })


    });



    loadFiles();

}




// ------------------------------
// CREAR CARPETA
// ------------------------------

async function createFolder(){



    let name =
    prompt(
    "Nombre de carpeta:"
    );



    if(!name)
    return;



    await fetch(
    "/api/folder",
    {

    method:"POST",

    headers:
    {
    "Content-Type":
    "application/json"
    },


    body:
    JSON.stringify({

        name:name

    })


    });



    alert(
    "Carpeta creada"
    );


    loadFiles();


}




// ------------------------------
// BUSCADOR
// ------------------------------

function searchFiles(){


    let text =
    document
    .getElementById("search")
    .value
    .toLowerCase();



    let filtered =
    allFiles.filter(

        f=>

        f.name
        .toLowerCase()
        .includes(text)

    );



    renderFiles(
        filtered
    );


}




// ------------------------------
// ESTADISTICAS
// ------------------------------

function updateStats(){



    document
    .getElementById("count")
    .textContent =
    allFiles.length;



    let total =
    0;



    allFiles.forEach(
        f=>
        total += f.size
    );



    document
    .getElementById("used")
    .textContent =
    formatSize(total);



    document
    .getElementById("status")
    .textContent =
    "ONLINE";

}



// ------------------------------
// FORMATEAR TAMAÑO
// ------------------------------

function formatSize(bytes){


    if(bytes < 1024)

    return bytes+" B";



    if(bytes < 1024*1024)

    return(
    (bytes/1024)
    .toFixed(1)
    +" KB"
    );



    return(
    (bytes/(1024*1024))
    .toFixed(2)
    +" MB"
    );


}




// ------------------------------
// ARRASTRAR ARCHIVOS
// ------------------------------

let drop =
document.getElementById(
"dropzone"
);



if(drop){


drop.addEventListener(
"dragover",
e=>{

e.preventDefault();

drop.style.background=
"rgba(56,189,248,.2)";

});


drop.addEventListener(
"dragleave",
()=>{

drop.style.background="";

});


drop.addEventListener(
"drop",
async e=>{


e.preventDefault();


let file =
e.dataTransfer.files[0];


if(!file)
return;



let form =
new FormData();



form.append(
"file",
file
);



await fetch(
"/api/upload",
{

method:"POST",

body:form

});



loadFiles();


});


}




// ------------------------------
// INICIO
// ------------------------------

window.onload =
function(){

    loadFiles();

};
