import {
  View,
  Text,
  SafeAreaView,
  ScrollView,
  Image,
  TouchableOpacity,
} from "react-native";
import React, { useEffect, useState } from "react";
import images from "../../constants/images";
import FormField from "../../components/FormField";
import { Link, router } from "expo-router";
import AsyncStorage from "@react-native-async-storage/async-storage";
import Toast from "react-native-toast-message";

const Login = () => {
  const [form, setForm] = useState({
    email: "",
    password: "",
  });
  const [isSubmitting, setisSubmitting] = useState(false);
  const apiUrl = process.env.EXPO_PUBLIC_API_URL;
  const [autoSignIn, setautoSignIn] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      const st = await AsyncStorage.getItem("session_token");
      const rt = await AsyncStorage.getItem("refresh_token");

      const userId = await AsyncStorage.getItem("userId");
      if (st !== null) {
        try {
          Toast.show({
            type: "info",
            text1: "Welcome back!",
            text2: "Automatically signing you in",
            visibilityTime: 200000,
          });
          const response = await fetch(apiUrl + "/auth/refreshsession", {
            method: "POST",
            headers: {
              Accept: "application/json",
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ refresh_token: rt, user_id: userId }),
          });
          const content = await response.json();
          await AsyncStorage.setItem("session_token", content["session_token"]);
          await AsyncStorage.setItem("email", content["email"]);
          router.push("/home");
        } catch (e) {
          setautoSignIn(false);
          Toast.show({
            type: "error",
            text1: "Error",
            text2: "Auto sign-in failed",
          });
          await AsyncStorage.removeItem("session_token");
          await AsyncStorage.removeItem("refresh_token");
          await AsyncStorage.removeItem("userId");
        }
      } else {
        setautoSignIn(false);
      }
    };

    const result = fetchData().catch(console.error);
  });

  const submit = async (e: any) => {
    e.disabled = true;
    if (form.email == "" || form.password == "") {
      alert("Email or password field empty");
      return;
    }

    try {
      if (isSubmitting) {
        return;
      }
      setisSubmitting(true);
      Toast.show({
        type: "info",
        text1: "Logging in",
        visibilityTime: 200000,
      });
      const loginResponse = await fetch(apiUrl + "/auth/login", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      });

      const loginContent = await loginResponse.json();
      if (loginResponse.status != 200) {
        setisSubmitting(false);
        alert("Login failed");
        return;
      }
      await AsyncStorage.setItem(
        "session_token",
        loginContent["session_token"],
      );
      await AsyncStorage.setItem("email", loginContent["email"]);
      // user change
      await AsyncStorage.setItem("userId", loginContent["user_id"]);
      await AsyncStorage.setItem(
        "refresh_token",
        loginContent["refresh_token"],
      );
      router.push("/home");
    } catch (e) {
      setisSubmitting(false);
      Toast.show({
        type: "error",
        text1: "Error",
        text2: "An error occurred",
        visibilityTime: 1000,
      });
    }
  };

  if (autoSignIn) {
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
                Signing you into Newsler!
              </Text>
            </View>
          </View>
        </ScrollView>
      </SafeAreaView>
    );
  } else {
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
                <Link
                  href="/signup"
                  className="font-medium text-lg text-primary"
                >
                  Sign up
                </Link>
              </View>
            </View>
          </View>
        </ScrollView>
      </SafeAreaView>
    );
  }
};

export default Login;
