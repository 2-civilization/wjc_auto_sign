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
  const [formData,setFormData] = useState({
    account:'',
    pswd:'',
    email:'',
    coordinates:'',
    emailVCode:''
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
      <PageSwitch nowSetp={nowSetp} setStep={setStep} formData={formData} setFormData={setFormData}/>
    </Flex>
  );
}

function PageSwitch({nowSetp,setStep,formData,setFormData}){
  switch (nowSetp) {
    case 0:
      return <RegPage setStep={setStep} setFormData={setFormData}/>;
    case 1:
      return <EmailCheckPage setStep={setStep} formData={formData} setFormData={setFormData}/>;
    case 2:
      return <SetCoordinatesPage setStep={setStep} formData={formData} setFormData={setFormData}/>;
    case 3:
      return <ResultPage />;
    default:
      return <RegPage setStep={setStep} setFormData={setFormData}/>;
  }
}











