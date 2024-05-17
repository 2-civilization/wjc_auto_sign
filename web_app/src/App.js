import { Flex,Steps,Typography } from 'antd';
import { UserAddOutlined,RobotOutlined,EnvironmentOutlined,SmileOutlined } from '@ant-design/icons';
import { useState } from 'react';
import RegPage from './RegPage';
import EmailCheckPage from './EmailCheckPage';
import SetCoordinatesPage from './SetCoordinatesPage';
import ResultPage from './ResultPage';

const { Title } = Typography;

export default function RegisterForm() {
  const [nowSetp,setStep] = useState(0);
  const [formData,setFromData] = useState({
    username:'',
    password:'',
    email:'',
    coordinates:''
  });

  return (
    <Flex vertical
      justify='center'
      align='center'
      gap='small'
      >
      <Title>Auto Sign</Title>
      <Steps 
        size='small'
        current={nowSetp}
        items={[
          {title:'填写账号信息',icon:<UserAddOutlined />},
          {title:'验证账号',icon:<RobotOutlined />},
          {title:'设置签到位置',icon:<EnvironmentOutlined />},
          {title:'完成注册',icon:<SmileOutlined />}
        ]}
      />
      <PageSwitch nowSetp={nowSetp} setStep={setStep} formData={formData} setFromData={setFromData}/>
    </Flex>
  );
}

function PageSwitch({nowSetp,setStep,formData,setFromData}){
  switch (nowSetp) {
    case 0:
      return <RegPage setStep={setStep} setFromData={setFromData}/>;
    case 1:
      return <EmailCheckPage setStep={setStep} formData={formData} setFromData={setFromData}/>;
    case 2:
      return <SetCoordinatesPage setStep={setStep} setFromData={setFromData}/>;
    case 3:
      return <ResultPage />;
    default:
      return <RegPage setStep={setStep} setFromData={setFromData}/>;
  }
}











