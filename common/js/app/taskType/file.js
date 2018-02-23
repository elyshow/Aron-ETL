$(function () {
//重置
     $('.reset').bind('click', function (){
         $('.form_reset').form('reset')
    })
//普通文件文件类型
	 $("#combo_type").combobox({
		valueField: 'value',
		textField: 'text',
		data: [{
			"value": 1,
			"text": "txt"
		}, {
			"value": 2,
			"text": "doc"
		}, {
			"value": 3,
			"text": "pdf"
		}, {
			"value": 4,
			"text": "jpg"
		}, {
			"value": 5,
			"text": "png"
		}, {
			"value": 6,
			"text": "csv"
		}, {
			"value": 7,
			"text": "xsl"
		}],
	})
//普通文件本地上传
    $("#btn_sub").linkbutton({
        onClick:function(){
            var checkText=$("#combo_type").combobox('getText');
			var checkFile=$("#file_type").filebox('getText');
			getFile=checkFile.split(".")[checkFile.split(".").length-1]
			if(checkText == getFile){
                var form = $("#basic_information").serializeArray();
			    $('#infoFile').form('submit',{
				    url:'/taskTypeDialog/',
				    onSubmit:function(param){
					   for(var i in form)
						  param[form[i].name] = form[i].value
					   return $(this).form('validate')
				    },
				    success:function(){
						$('#tb').tabs('close','普通文件本地上传');
						$('.form_reset').form('reset');
                  	    $("#taskTypeDialog").dialog('close');
					    $('#sjyglList').datagrid('reload');
				}
			})
			}
			else{
				$.messager.alert('警告','请上传正确的文件格式','warning');
				return false;
			}

        }
    })

//普通文件远程下载
    $("#taskDownload").linkbutton({
        onClick:function(){
            var info=$("#basic_information").serialize();
			var downloadFile=$("#downloadFile").serialize();
			$.ajax({
				url:'/taskTypeDialog/taskDownloadDialog/',
				data:downloadFile+'&'+info,
				type:'get',
				datatype:'json',
				success:function(){
					$('#tb').tabs('close','普通文件远程下载');
					$('.form_reset').form('reset');
					$('#taskTypeDialog').dialog('close');
					$('#sjyglList').datagrid('reload');
				}

			})
			}
    })
//上传数据库文件
    $("#sqlSub").linkbutton({
        onClick:function(){
            var sqlType=$("#sqlType").combobox('getText');
			var subSqlType=$("#subSqlType").filebox('getText');
			getSql=subSqlType.split(".")[subSqlType.split(".").length-1]

			if(sqlType == getSql){
                var form = $("#basic_information").serializeArray();
			    $('#infoSql').form('submit',{
				    url:'/taskTypeDialog/taskSqlDialog/',
				    onSubmit:function(param){
					   for(var i in form)
						  param[form[i].name] = form[i].value
					   return $(this).form('validate')
				    },
				    success:function(){
						$('#tb').tabs('close','数据库文件');
						$('.form_reset').form('reset');
                  	    $("#taskTypeDialog").dialog('close');
					    $('#sjyglList').datagrid('reload');
				}
			})
			}
			else{
				$.messager.alert('警告','请上传正确的文件格式','warning');
				return false;
			}

        }
    })


//添加字段下一步　 添加任务刷新频率
	$('#addField_nextStep').linkbutton({
		onClick:function(){
			while($('#tb').tabs('exists',4)){
			$('#tb').tabs('close',4);
		}
			$('#tb').tabs('add', {
	 		title: '设置任务刷新频率',
			href : '/taskType/getContent/taskRefresh',
	 	});
		}
	})


// 数据接口类型数据上传上去,继而读出库里面的表,追加添加表
	$('#data_nextStep').linkbutton({
		onClick:function () {

			while($('#tb').tabs('exists',2)){
			$('#tb').tabs('close',2);
		}
			var dataFile=$('#dataInterFile').serialize();
			// var tableNameForm=$('#tableNameForm').serialize();
			console.log(dataFile)
			$('#tb').tabs('add', {
	 			title: '添加表',
				href : '/taskType/getContent/addTable/?'+dataFile,
	 		});

		}
	})

// 把选中的表上传，继而读出字段名称
	$('#addTable_nextStep').linkbutton({
		onClick:function () {
			while($('#tb').tabs('exists',3)){
			$('#tb').tabs('close',3);
		}
			var tableNameForm=$('#tableNameForm').serialize();
			var dataFile=$('#dataInterFile').serialize();
			$('#tb').tabs('add', {
	 			title: '添加字段',
				href : '/taskType/getContent/addField/?'+tableNameForm+'&'+dataFile,
	 		});

		}
	})
//点击完成
	$('#taskRefresh_nextStep').linkbutton({
		onClick:function () {
			var form = $("#basic_information").serialize();
			var dataFile=$('#dataInterFile').serialize();
			var tableNameForm=$('#tableNameForm').serialize();
			var fieldToForm=$('#fieldToForm').serialize();
			var refresh = $("#taskRefresh").serialize();
			$.ajax({
				url:'/taskTypeDialog/fieldToDialog/',
				data:form+'&'+dataFile+'&'+tableNameForm+'&'+fieldToForm+'&'+refresh,
				type:'get',
				gatatype:'json',
				success:function (ret) {
					$('.form_reset').form('reset');
					$("#taskTypeDialog").dialog('close');
					$('#sjyglList').datagrid('reload');

				}
			})

		}
	})

	$('#apida_sub').linkbutton({
		onClick:function () {
			var form = $("#basic_information").serialize();
			var infoApi = $("#infoApi").serialize();
			$.ajax({
				url:'/taskTypeDialog/dataApiDialog/',
				data:form+'&'+infoApi,
				type:'get',
				datatype:'json',
				success:function (ret) {
					$('#tb').tabs('close','API接口');
					$('.form_reset').form('reset');
					$("#taskTypeDialog").dialog('close');
					$("#sjyglList").datagrid('reload');

				}

			})

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

//测试
function dataTest() {
	var data = '';
	$('#dataInterFile').form('submit', {
		url: "/taskTypeDialog/dataTest/",
		type:"GET",
		dataType:"JSON",
		onSubmit: function () {
			return true
		},
		success: function (data) {
			if (data==1) {
				$.messager.confirm('提示', '连接成功', 'warning');
			}
			else{

				$.messager.confirm('提示', '连接失败，请重新配置', 'warning');
			}
		}

	});
}

//API 接口调用方法
        $(".get_type").combobox({
		valueField: 'value',
		textField: 'text',
		data: [{
			"value": 1,
			"text": "Get",
		},{
			"value": 2,
			"text": "Post"
		}],
	})
//API　接口文件类型
        $(".post_type").combobox({
		valueField: 'value',
		textField: 'text',
		data: [{
			"value": 1,
			"text": "Xml",
		},{
			"value": 2,
			"text": "Json"
		}],
	})

