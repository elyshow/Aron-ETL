$(function () {
	$('#refreshModifyBtn').linkbutton({
		onClick:function(){
			$('#tt').tabs('enableTab', 1);
			$('#tt').tabs('select', 1);
		}
	})
	//任务刷新频率
    $('input[name="FreSetting"]').change(function(){
        if($(this).is(":checked"))
            var index = $(this).index()
    //     $(this).is(":checked")
    //     var index = $(this).index()
        switch (index){
            case 0:
                $('.month_day,.play_time').show();
                $('.week_day').hide();
                $('#cycle').next().show().end().combobox('enableValidation');
                $('#once_time').datetimebox('disableValidation').next().hide();
                $('#hours,#minutes').next().show().end().combobox('enableValidation');
                $('#interval_day,#days').combobox('disableValidation').next().hide();
                if( $('#cycle').combobox('getValue') == 1 ){
                    $('#days').next().show().end().combobox('enableValidation');
                }else if($('#cycle').combobox('getValue') == 2){
                    $('#days').combobox('disableValidation').next().hide();
                    $('.week_day').show()
                }
                $('.words').hide();
                break;
            case 1:
                $('.month_day').show();
                $('#days,#interval_day,#cycle,#hours,#minutes').combobox('disableValidation').next().hide();
                $('.words,.play_time,.week_day').hide();
                $('#once_time').next().show().end().datetimebox('enableValidation');
                break;
            case 2:
                $('#cycle,#days,#interval_day,#hours,#minutes').combobox('disableValidation');
                $('#once_time').datetimebox('disableValidation').next().hide();
                $('.month_day,.week_day').hide();
                $('.play_time,.words').hide();
                break;
            case 3:
                $('.month_day,.play_time').show();
                $('#interval_day,#hours,#minutes').next().show().end().combobox('enableValidation');
                $('#once_time').datetimebox('disableValidation').next().hide();
                 $('#cycle,#days').combobox('disableValidation').next().hide();
                $('.words,.week_day').hide();
                break;
        }
    })



 function selectCycle(record){
    $(this).combobox('checkSelect',$(this));
    switch (record.value){
        case 1:
            $('#days').next().show().end().combobox('enable').combobox('enableValidation');
            $('.week_day').hide();
            break;
        case 2:
            $('#days').combobox('disableValidation').combobox('disable').next().hide();
            $('.week_day').show();
            break;
        case 3:
            $('.week_day').hide();
            $('#days').combobox('disableValidation').combobox('disable').next().hide();

            break;
    }
}
    
	$('input[name="FreSetting"]').change()


})

function initComboBox(start, length){
    var list = [];
    for(var i = 0; i < length; i++,start++){
        list[i] = {};
        list[i].value = "'" +start + "'";
        list[i].text = String(start)
    }
    return list;
}

function selectCycle(record){
    $(this).combobox('checkSelect',$(this));
    switch (record.value){
        case 1:
            $('#days').next().show().end().combobox('enable').combobox('enableValidation');
            $('.week_day').hide()
            break;
        case 2:
            $('#days').combobox('disableValidation').combobox('disable').next().hide();
            $('.week_day').show()
            break;
        case 3:
            $('.week_day').hide()
            $('#days').combobox('disableValidation').combobox('disable').next().hide();

            break;
    }
}

