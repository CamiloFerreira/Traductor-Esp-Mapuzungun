$(document).ready(function() {
	
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


	//Llena con todas las palabras

	$.each(res,function(i,item){
		

		cad = $("tbody").html(); 



		var lista = item['palabras']
		var letra = item['letra']


		for (var i = 0; i < lista.length; i++) 
		 {
		 		var palabra     =  lista[i]['palabra'];
		 		var significado = lista[i]['significado'];
		 		
				cad += "<tr class='"+letra+"'>" 
		 		cad += "<td class='pal'>"+palabra.join()+"</td>" 
		 		cad += "<td class='sig'>"+significado.join()+"</td>" 
		 		cad += "</th>"


		 }		

		
		$("tbody").html(cad); 

		 
	})


	$("#input").keyup(function(){
		var cadena = $("#input").val().toLowerCase();
		var sel    = $("select").val();

		if(sel == "1"){
			$("#data tr").each(function(){
				var sig = $(this).find(".sig").text().toLowerCase();


				if(sig.includes(cadena)){
					$(this).show()
				}else{
					$(this).hide();
				}

			})
		}else{
			$("#data tr").each(function(){
				var sig = $(this).find(".pal").text().toLowerCase();

				if(sig.includes(cadena)){
					$(this).show()
				}else{
					$(this).hide();
				}

			})
		}

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

		$("#data tr").each(function(){
			if ( letra != $(this).attr('class')){

				$(this).hide();
			}else{
				$(this).show();
			}
		})
	})

});