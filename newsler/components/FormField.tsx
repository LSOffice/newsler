import { View, Text, TextInput, TouchableOpacity } from 'react-native'
import React, { useState } from 'react'
import { Eye, EyeOff } from 'lucide-react-native'

const FormField = (
    { title, value, handleChangeText, otherStyles, ...props }
    : 
    {
        title: string
        value: string
        handleChangeText: any,
        otherStyles: string
    }) => {
    const [showPassword, setshowPassword] = useState(false)
  
    return (
        <View className={`space-y-2 ${otherStyles}`}>
            <Text className='text-base text-slate-600 font-medium'>{title}</Text>

            <View className='border-2 border-black w-full h-10 px-4 bg-black-100 rounded-2xl focus:border-primary items-center justify-center flex flex-row'>
                <TextInput
                    className='text-black h-full items-center font-semibold text-base flex justify-center flex-1'
                    value={value}
                    onChangeText={handleChangeText}
                    secureTextEntry={title === 'Password' && !showPassword}
                />

                {
                    title === 'Password' && 
                    (
                        <TouchableOpacity onPress={() => setshowPassword(!showPassword)}>
                            {!showPassword ? <Eye className='text-primary w-6 h-6'/> : <EyeOff className='text-primary w-6 h-6'/>}
                        </TouchableOpacity>
                    )
                }
            </View>
        </View>
    )
}

export default FormField