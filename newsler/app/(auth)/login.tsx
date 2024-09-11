import {
  View,
  Text,
  SafeAreaView,
  ScrollView,
  Image,
  TouchableOpacity,
} from "react-native";
import React, { useState } from "react";
import images from "../../constants/images";
import FormField from "../../components/FormField";
import { Link, router } from "expo-router";

const Login = () => {
  const [form, setForm] = useState({
    email: "",
    password: "",
  });
  const [isSubmitting, setisSubmitting] = useState(false);

  const submit = () => {
    router.push("/home");
  };

  return (
    <SafeAreaView className="bg-white h-full w-full">
      <ScrollView contentContainerStyle={{ height: "100%", width: "100%" }}>
        <View className="w-full justify-center min-h-[90vh] ">
          <View className="flex flex-col gap-2">
            <View className="flex flex-row items-center gap-2">
              <Image
                source={images.logo}
                className="w-14 h-14"
                resizeMode="contain"
              />
              <Text className="text-3xl text-primary font-bold text-center">
                Newsler
              </Text>
            </View>
            <Text className="text-xl font-semibold pl-4">
              Sign-in to Newsler
            </Text>
          </View>

          <View className="px-4 mt-5">
            <FormField
              title="Email"
              value={form.email}
              handleChangeText={(e: string) => setForm({ ...form, email: e })}
              otherStyles=""
            />

            <FormField
              title="Password"
              value={form.password}
              handleChangeText={(e: string) =>
                setForm({ ...form, password: e })
              }
              otherStyles="mt-2"
            />

            <TouchableOpacity
              activeOpacity={0.7}
              onPress={submit}
              disabled={isSubmitting}
              className={`bg-primary rounded-xl h-10 justify-center items-center w-full mt-5 ${isSubmitting ? "opacity-50" : ""}`}
            >
              <Text className="text-white font-semibold text-lg">Login</Text>
            </TouchableOpacity>

            <View className="justify-center pt-5 flex-row gap-1">
              <Text className="text-lg text-black font-light">
                Don't have an account?
              </Text>
              <Link href="/login" className="font-medium text-lg text-primary">
                Sign up
              </Link>
            </View>
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

export default Login;
