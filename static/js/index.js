	function getTrad(input){
		//Se obtiene el texto ingresado para ser mandado a python
		var dic = {cadena :input};
		$.ajax({
			url:"/gText",
			type:"POST",
	  		data : JSON.stringify(dic),
	    	contentType: "application/json",

	    	success:function(response){
	    		var json = $.parseJSON(response);
	    		console.log(json); 
	    		$("#map").text(json.t);
	    	},
	    	error:function(response){
	    		console.log("Ha sucedido un problema");
	    	}

		});
	}
$(document).ready(function(){


		$(".pop_menu").hide();


		var height = screen.height;
		var img_h = height / 1.6;
		

		$("body").css({'height':height});
		$("#fondo").css({'height':height});
		$("img").css({'height':img_h});
		
		//Se carga el json que contiene los nombres de las imagenes
		$.getJSON("/static/img/imagenes.json",function(data){
			var i = Math.floor(Math.random() * data.length);
			var dir = "/static/img/"+data[i].imagen;
			$("img").attr("src",dir);
			$("#descripcion").text(data[i].descripcion);
		});

		//Se carga el archivo
		$("input").change(function(){	
			let file =  document.getElementById("file").files[0];
	  		let reader = new FileReader();

	  		var txt = "";

	  		reader.readAsText(file);

	  		//Se carga el texto del archivo y es enviado
	 		reader.onload = function() {

	 			var texto = reader.result;
	 			getTrad(texto);
	 		};
		});


		//Se detecta cuando se escribe 
		$("#textIdioma").on("keyup",function(){
			var texto = $("#textIdioma").val();

			if(texto != ""){
			console.log(texto);
			getTrad(texto);				
			}

		})

		//Funciones de los botones
		activo = false;
		$("#btn-dic").click(function(){

			$(".pop_menu").css({'opacity':"100%"});
			if(activo == true){
				$(".pop_menu").slideUp("slow");
				activo = false
			}else{
				$(".pop_menu").slideDown("slow");
				activo = true;
			}
		});


		//Funciones del diccionario 
		//_-----------------------------------------

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
		var sel    = $("#dic_sel").val();

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
	});





	})