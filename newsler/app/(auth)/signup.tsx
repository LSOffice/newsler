import { View, Text, ScrollView, Image, TouchableOpacity } from "react-native";
import React, { useEffect, useState } from "react";
import { SafeAreaView } from "react-native-safe-area-context";
import images from "../../constants/images";
import FormField from "../../components/FormField";
import { Link, router } from "expo-router";
import AsyncStorage from "@react-native-async-storage/async-storage";
import Toast from "react-native-toast-message";

const SignUp = () => {
  const [form, setForm] = useState({
    email: "",
    password: "",
  });
  const [isSubmitting, setisSubmitting] = useState(false);
  const apiUrl = process.env.EXPO_PUBLIC_API_URL;

  useEffect(() => {
    const fetchUserId = async () => {
      const userId = await AsyncStorage.getItem("userId");
      if (userId !== null) {
        router.push("/login");
      }
    };

    const result = fetchUserId().catch(console.error);
  });

  const submit = async (e: any) => {
    if (form.email == "" || form.password == "") {
      Toast.show({
        type: "error",
        text1: "Error",
        text2: "Email or password field empty",
      });
      return;
    }

    if (form.password.length < 8) {
      Toast.show({
        type: "error",
        text1: "Error",
        text2: "Password has to be more than 8 characters",
      });
      return;
    }

    try {
      Toast.show({
        type: "info",
        visibilityTime: 200000,
        text1: "Signing up",
        text2: "Give it a bit",
      });
      const response = await fetch(apiUrl + "/auth/signup", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      });

      const content = await response.json();
      if (!content["signup"]) {
        Toast.show({
          type: "error",
          visibilityTime: 2000,
          text1: "Sign up failed",
          text2: "(Account not created - register failed)",
        });
        return;
      }
      await AsyncStorage.setItem("userId", content["user_id"]);

      const loginResponse = await fetch(apiUrl + "/auth/login", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      });
      if (loginResponse.status != 200) {
        Toast.show({
          type: "error",
          visibilityTime: 2000,
          text1: "Sign up failed",
          text2: "(Account created - login failed)",
        });
        return;
      }
      const loginContent = await loginResponse.json();

      Toast.show({
        type: "success",
        visibilityTime: 200,
        text1: "You're all signed up",
        text2: "Welcome to Newsler!",
      });

      await AsyncStorage.setItem(
        "session_token",
        await loginContent["session_token"],
      );
      await AsyncStorage.setItem("userId", await loginContent["user_id"]);
      await AsyncStorage.setItem(
        "refresh_token",
        await loginContent["refresh_token"],
      );
      await AsyncStorage.setItem("email", loginContent["email"]);
      router.push("/home");
    } catch (e) {
      Toast.show({
        type: "error",
        text1: "Error",
        text2: "An error occurred",
        visibilityTime: 1000,
      });
    }
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
              Sign-up to Newsler
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
              <Text className="text-white font-semibold text-lg">Sign up</Text>
            </TouchableOpacity>

            <View className="justify-center pt-5 flex-row gap-1">
              <Text className="text-lg text-black font-light">
                Have an account?
              </Text>
              <Link href="/login" className="font-medium text-lg text-primary">
                Login
              </Link>
            </View>
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

export default SignUp;
