import { Form,Input,message,Typography } from 'antd';
import { useState } from 'react';
import Link from 'antd/es/typography/Link';
const { Title,Text } = Typography;

export default function EmailCheckPage(props){
    const [form] = Form.useForm();
    const [isAlready, setIsAlready] = useState(false);
    const [otpStatus, setOtpStatus] = useState("");

    async function checkEmail(){
        setIsAlready(true);
        if(await emailOnlineCheck(props.formData.email,form.getFieldValue("validateCode"))){
        message.info("邮箱验证成功！");
        props.setStep(2);
        }else{
        message.error("验证码不正确！");
        setOtpStatus("error");
        setIsAlready(false);
        form.setFieldsValue({'validateCode':""});
        }
    }

    return (
        <>
        <Title level={3}>验证邮箱</Title>
        <Text>一封包含验证码的邮件已发送至你的邮箱<Text strong>{props.formData.email}</Text>，填写验证码以验证邮箱。</Text>
        <Form
            size='large'
            form={form}
        >
            <Form.Item name='validateCode'>
            <Input.OTP 
                onChange={async () =>{await checkEmail();}}
                disabled={isAlready}
                status={otpStatus}
            />
            </Form.Item>
        </Form>
        <Link onClick={() => props.setStep(0)}>返回上一步</Link>
        </>
    );
}
  
async function emailOnlineCheck(email,validateCode){
    const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay));
    await sleep(3000);
    if(validateCode === "123456"){
        return true;
    }else{
        return false;
    }
}