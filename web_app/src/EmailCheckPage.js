import { Form,Input,message,Typography } from 'antd';
import { useState } from 'react';
import Link from 'antd/es/typography/Link';
import axios from 'axios';
const { Title,Text } = Typography;

export default function EmailCheckPage(props){
    const [form] = Form.useForm();
    const [isAlready, setIsAlready] = useState(false);
    const [otpStatus, setOtpStatus] = useState("");

    async function checkEmail(){
        setIsAlready(true);
        const setStep = props.setStep;
        const account = props.formData.account;
        const validateCode = form.getFieldValue("validateCode");
        axios.post('/emailCheck',
            {
                account:account,
                emailVCode:validateCode
            },
            {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }
        ).then(res => {
            if(res.data.code === 'ok'){
                message.success(res.data.msg);
                setStep(2);
            }else{
                message.error(res.data.msg);
                setOtpStatus("error");
                setIsAlready(false);
                form.setFieldsValue({'validateCode':""});
            }
        }).catch(err => {
            message.error("与服务器连接失败");
            console.log(err);
        });
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
  