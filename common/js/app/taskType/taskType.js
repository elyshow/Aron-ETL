$(function() {
	$("#combo_list").combobox({
		valueField: 'value',
		textField: 'text',
		data: [{
			"value": "1",
			"text": "普通文件本地上传"
		},
			{
			"value": "5",
			"text": "普通文件远程下载"
		},
			{
			"value": "2",
			"text": "数据库文件"
		}, {
			"value": "3",
			"text": "数据接口"
		}, {
			"value": "4",
			"text": "API接口"
		}],
	})

	$('.basic_next').bind('click', function () {
		$('#basic_information').form('submit', {
		url: "/taskTypeDialog/tasknameTest/",
		type:"GET",
		dataType:"JSON",
		onSubmit: function () {
			return true
		},
		success: function (data) {
			if (data==1) {

		var a = $("#combo_list").combobox('getText');
		if (a == "普通文件本地上传") {
			var title = "普通文件本地上传";
			var url = "/taskType/getContent/file";

		}
		else if (a == "普通文件远程下载") {
			var title = "普通文件远程下载";
			var url = '/taskType/getContent/fileDownload'

		}
		else if (a == "数据库文件") {
			var title = "数据库文件";
			var url = '/taskType/getContent/sqlfile'

		}
		else if (a == "数据接口") {
			var title = "数据接口";
			var url = '/taskType/getContent/datainterface'

		}
		else if (a == "API接口") {
			var title = "API接口";
			var url = '/taskType/getContent/apiinterface'
		} else {
			$.messager.alert('警告', "请选择文件类型!", 'warning');
			return false;
		}
		i = 1;
		while($('#tb').tabs('exists',i)){
			$('#tb').tabs('close',i);

		}
		$('#tb').tabs('add', {
			title: title,
			href: url,

		});
			}
			else{

				$.messager.confirm('提示', '任务名已存在，请重填', 'warning');
			}
		}

	});


	})

})





