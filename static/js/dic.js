$(document).ready(function() {
	
	var height = $(window).height(); // Obtiene el tamaño de la pantalal
	var res ;
	$('section').height(height);

	$("#mostrar").css('height',height/2);
	//Carga las palabras al comenzar la pagina
	var datos = $.ajax({
			async: false, // permite guardar la variable de response como global
			url:"/gDic",
			type:"POST",
        	contentType: "application/json",

        	success:function(response){
        		 res = $.parseJSON(response);
        	},
        	error:function(response){
        		console.log("Ha sucedido un problema");
        	}

		})


	//Llena con la primera posicion de palabras osea "a"

	$.each(res,function(i,item){
		
		//Recorre cada fila para la letra "a"
		cad = ""
		for(var i =0 ; i < item.a.length ; i++)
		{
			lista = item.a[i];

			palabra = item.a[i][0];
			significado = item.a[i][1];

			cad += "<tr>" 
			cad += "<td>"+palabra+"</td>" 
			cad += "<td>"+significado+"</td>" 
			cad += "</th>"
			
		}
		$("tbody").html(cad); 
	})



	$("#buscar").click(function (evt) {

		//Se obtiene el texto ingresado para ser mandado a python
		var dic = {cadena :$("#texto").val()};	
	})


	// Añadir animacion a li

	$(".li")
	.mouseover(function(){
		$(this).css('color',"#215DDC");
		$(this).css('text-decoration-line','underline');
	})
	.mouseout(function(){
		$(this).css("color","#27BBFF");
		$(this).css('text-decoration-line','none');
	})
	.click(function(){
		var letra = $(this).text().trim();

		$.each(res,function(i,item){
				

				//Recorre cada fila para la letra "a"
				$("tbody").html(" ");
				cad = ""

				for(var i =0 ; i < item[letra].length ; i++)
				{
					lista = item[letra][i];

					palabra = item[letra][i][0];
					significado = item[letra][i][1];

					cad += "<tr>" 
					cad += "<td>"+palabra+"</td>" 
					cad += "<td>"+significado+"</td>" 
					cad += "</th>"
					
				}
				$("tbody").html(cad); 
			})
	})

});