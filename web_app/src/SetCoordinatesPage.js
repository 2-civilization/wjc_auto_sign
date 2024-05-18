import { Form,message,Typography,Button,Select } from 'antd';
import axios from 'axios';
import { useState } from 'react';
const { Title,Text } = Typography;

export default function SetCoordinatesPage(props){
    const coordinatesList = getCoordinatesList();
  
    const selectCoordinates = [];
    for(let key in coordinatesList){
      selectCoordinates[key]={
        value:coordinatesList[key].longitude+','+coordinatesList[key].latitude,
        label:coordinatesList[key].name
      };
    }
    // const [chooseCLabel,setChooseCLabel] = useState(selectCoordinates[0].label);
    const [chooseCValue,setChooseCValue] = useState(selectCoordinates[0].value);
    const [form] = Form.useForm();
    
    function changeCValue(){
      const coordinates = form.getFieldValue("coordinates");
      setChooseCValue(coordinates);
    }
    function setCoordinates(){
      // props.setFormData({
      //   coordinates:chooseCValue
      // })
      const setStep = props.setStep;
      const account = props.formData.account;
      // const coordinates = props.formData.coordinates;
      axios.post('/submit',{
        account:account,
        coordinate:chooseCValue
      },{
        headers: {
        'Content-Type': 'multipart/form-data'
      }
    }).then(res=>{
        if(res.data.code==='ok'){
          message.success(res.data.msg);
          setStep(3);
        }else{
          message.error(res.data.msg);
        }
      })
      .catch(error=>{
        message.error("与服务器连接失败");
        console.log(error);
      })
    }
    return (
      <>
        <Title level={3}>最后一步</Title>
        <Text>设置你希望签到的位置</Text>
        <Form 
          form={form}
          
          >
          <Form.Item name="coordinates">
            <Select 
              defaultValue={selectCoordinates[0].value}
              options={selectCoordinates}
              onChange={changeCValue}
            />
          </Form.Item>
          <Form.Item>
            <Text>{ chooseCValue }</Text>
          </Form.Item>
        </Form>
        <Button
            type="primary"
            onClick={setCoordinates}
            
          >
            确认
          </Button>
      </>
    );
  }
  
  function getCoordinatesList(){
    //const res = await axios.get('./public/local.json');
    const res = [
      {
        "name": "学校 签到位置",
        "longitude": "118.265303",
        "latitude": "31.359218"
      },
      {
        "name": "(14)会堂",
        "longitude": "118.265817",
        "latitude": "31.360045"
      },
      {
        "name": "(20)20号宿舍",
        "longitude": "118.26722",
        "latitude": "31.361751"
      },
      {
        "name": "(19)19号宿舍",
        "longitude": "118.265968",
        "latitude": "31.361062"
      },
      {
        "name": "(18)18号宿舍",
        "longitude": "118.264626",
        "latitude": "31.360441"
      },
      {
        "name": "(16)16号宿舍",
        "longitude": "118.262517",
        "latitude": "31.360803"
      },
      {
        "name": "(17)研究生宿舍",
        "longitude": "118.263445",
        "latitude": "31.361708"
      },
      {
        "name": "(13)产教融合研究中心",
        "longitude": "118.264182",
        "latitude": "31.358646"
      },
      {
        "name": "(26)专家楼",
        "longitude": "118.270022",
        "latitude": "31.355893"
      },
      {
        "name": "(25)教师公寓",
        "longitude": "118.27067",
        "latitude": "31.356312"
      },
      {
        "name": "(23)学术交流中心",
        "longitude": "118.269707",
        "latitude": "31.356606"
      },
      {
        "name": "一食堂",
        "longitude": "118.264394",
        "latitude": "31.359275"
      },
      {
        "name": "二食堂",
        "longitude": "118.267008",
        "latitude": "31.360011"
      },
      {
        "name": "(4)实训工厂",
        "longitude": "118.26285",
        "latitude": "31.358094"
      },
      {
        "name": "(3)汽车学院",
        "longitude": "118.26283",
        "latitude": "31.357774"
      },
      {
        "name": "(2)智能制造学院",
        "longitude": "118.26283",
        "latitude": "31.357775"
      },
      {
        "name": "(1)新材料与环保学院",
        "longitude": "118.26283",
        "latitude": "31.357776"
      },
      {
        "name": "(5)公共教学楼1",
        "longitude": "118.264091",
        "latitude": "31.35725"
      },
      {
        "name": "(6)公共教学楼2",
        "longitude": "118.266594",
        "latitude": "31.356948"
      },
      {
        "name": "(7)微电子院",
        "longitude": "118.26722",
        "latitude": "31.356577"
      },
      {
        "name": "(10)信息技术学院",
        "longitude": "118.267442",
        "latitude": "31.358758"
      },
      {
        "name": "(11)音乐艺术学院",
        "longitude": "118.268411",
        "latitude": "31.358249"
      },
      {
        "name": "(8)人文与社会学院",
        "longitude": "118.267099",
        "latitude": "31.358042"
      },
      {
        "name": "(9)学前教育学院",
        "longitude": "118.268027",
        "latitude": "31.35762"
      },
      {
        "name": "(21)体育馆",
        "longitude": "118.268673",
        "latitude": "31.359571"
      }
    ];
    return res;
  }