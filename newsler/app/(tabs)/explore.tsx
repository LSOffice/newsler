import { View, Text, TextInput, Image, SafeAreaView } from "react-native";
import React, { useState } from "react";
import FormField from "../../components/FormField";
import images from "../../constants/images";
import { LucideSearch } from "lucide-react-native";

const Explore = () => {
  const [form, setForm] = useState({
    query: "",
  });
  return (
    <SafeAreaView className="bg-white h-full w-full flex-1">
      <View className="flex flex-col">
        <View className="flex flex-row items-center gap-2 justify-center">
          <Image
            source={images.logo}
            className="w-10 h-10"
            resizeMode="contain"
          />
          <Text className="text-2xl text-primary font-bold text-center">
            Newsler
          </Text>
        </View>
        <View className="px-3 flex flex-col">
          <Text className="text-sm">Quick Search</Text>
          <View className="border border-black w-full mt-1 h-12 px-2 bg-black-100 rounded-2xl focus:border-primary items-center flex flex-row">
            <LucideSearch className="text-primary mr-2" />
            <TextInput
              className="text-black h-full items-center text-sm flex justify-center"
              value={form.query}
              onChangeText={(e: string) => setForm({ ...form, query: e })}
              secureTextEntry={false}
              placeholder="Joe Biden blunders again #LetsGoBrandon"
              placeholderTextColor={"gray"}
            />
          </View>
          <View className="flex flex-col w-full mt-2 h-full">
            <View className="border flex flex-row">
              <Text>abcd</Text>
            </View>
          </View>
        </View>
      </View>
    </SafeAreaView>
  );
};

export default Explore;
