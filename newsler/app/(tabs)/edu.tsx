import {
  View,
  Text,
  SafeAreaView,
  Image,
  TextInput,
  TouchableOpacity,
  ScrollView,
  Touchable,
  ActivityIndicator,
} from "react-native";
import React, { useEffect, useState } from "react";
import images from "../../constants/images";
import {
  LucideBookOpen,
  LucideCheck,
  LucidePaperclip,
  LucideRocket,
  LucideSearch,
  LucideSend,
} from "lucide-react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { Dropdown } from "react-native-element-dropdown";

const Education = () => {
  const [joinform, setjoinForm] = useState({
    classroom_code: "",
  });
  const [createForm, setcreateForm] = useState({
    classroom_name: "",
    subject_code: "",
    educational_level: "primary",
  });
  const [classroomList, setClassroomList] = useState([]);
  const [userType, setUserType] = useState("student");
  const apiUrl = process.env.EXPO_PUBLIC_API_URL;
  const [isLoading, setisLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        let loading = true;
        setisLoading(true);
        while (loading) {
          const response = await fetch(apiUrl + "/edu/load", {
            method: "POST",
            headers: {
              Accept: "application/json",
              "Content-Type": "application/json",
              Authorization:
                "Bearer " + (await AsyncStorage.getItem("session_token")),
            },
            body: JSON.stringify({
              user_id: await AsyncStorage.getItem("userId"),
            }),
          });
          if (response.status === 308) {
            const newResponse = await fetch(apiUrl + "/auth/refreshsession", {
              method: "POST",
              headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                refresh_token: await AsyncStorage.getItem("refresh_token"),
                user_id: await AsyncStorage.getItem("userId"),
              }),
            });
            const content = await newResponse.json();
            await AsyncStorage.setItem(
              "session_token",
              content["session_token"],
            );
            continue;
          }
          loading = false;
          const responseJson = await response.json();
          setClassroomList(responseJson["classrooms"]);
          setUserType(responseJson["edu_type"]);
          setisLoading(false);
        }
      } catch {}
    };

    fetchData();
  }, []);

  if (isLoading) {
    return (
      <View className="w-full h-full flex justify-center items-center">
        <ActivityIndicator color="black" className="mb-3" />
      </View>
    );
  } else {
    return (
      <SafeAreaView className="bg-white h-full w-full flex-1">
        <View className="flex flex-row items-center justify-center">
          <Image
            source={images.logo}
            className="w-10 h-10"
            resizeMode="contain"
          />
          <Text className="ml-2 text-2xl text-primary font-bold text-center">
            Newsler
          </Text>
          <Text className="mt-auto text-primary">EDU</Text>
        </View>
        {/* if no classrooms present in user list and they are a student */}
        {classroomList.length == 0 && userType == "student" ? (
          <View className="w-full h-[95%] items-center justify-center flex px-6">
            <Text className="text-primary font-bold text-2xl w-full text-left">
              Join a classroom
            </Text>
            <View className="border border-black w-full mt-1 h-12 bg-black-100 rounded-b-2xl rounded-tr-2xl focus:border-primary items-center flex flex-row">
              <TextInput
                className="text-black h-full px-4 items-center text-sm flex justify-center"
                value={joinform.classroom_code}
                onChangeText={(e: string) =>
                  setjoinForm({ ...joinform, classroom_code: e })
                }
                secureTextEntry={false}
                placeholder="Enter a class code... (e.g. ABC123)"
                placeholderTextColor={"gray"}
              />
            </View>
            <TouchableOpacity className="bg-primary mt-3 w-1/2 flex items-center justify-center rounded-2xl py-2">
              <Text className="text-white font-semibold text-lg">Join</Text>
            </TouchableOpacity>
            <View className="flex flex-col mt-7">
              <Text className="font-semibold">Are you a teacher?</Text>
              <Text className="mt-1">
                The current account is setup to be a student account. If you
                want to modify this, please contact support.
              </Text>
            </View>
          </View>
        ) : classroomList.length == 0 && userType == "teacher" ? (
          // if no classrooms in user list and type is teacher

          <View className="w-full h-[95%] items-center justify-center flex px-6">
            <Text className="text-primary font-bold text-2xl w-full text-left">
              Create a classroom
            </Text>
            <View className="w-full mt-4">
              <Text className="text-gray-600 text-xs">Classroom name</Text>
              <View className="border border-black w-full mt-1 h-10 bg-black-100 rounded-b-2xl rounded-tr-2xl focus:border-primary items-center flex flex-row">
                <TextInput
                  className="text-black h-full px-4 items-center text-base flex justify-center"
                  value={createForm.classroom_name}
                  onChangeText={(e: string) =>
                    setcreateForm({ ...createForm, classroom_name: e })
                  }
                  secureTextEntry={false}
                  placeholder="Enter a classroom name here"
                  placeholderTextColor={"gray"}
                />
              </View>
            </View>
            <View className="w-full mt-2">
              <Text className="text-gray-600 text-xs">Subject code</Text>
              <View className="border border-black w-full mt-1 h-10 bg-black-100 rounded-b-2xl rounded-tr-2xl focus:border-primary items-center flex flex-row">
                <TextInput
                  className="text-black h-full px-4 items-center text-base flex justify-center"
                  value={createForm.subject_code}
                  onChangeText={(e: string) =>
                    setcreateForm({ ...createForm, subject_code: e })
                  }
                  secureTextEntry={false}
                  placeholder="Enter a subject code here"
                  placeholderTextColor={"gray"}
                />
              </View>
            </View>
            <View className="w-full mt-2">
              <Text className="text-gray-600 text-xs">Educational Level</Text>
              <Dropdown
                style={{
                  borderColor: "black",
                  borderWidth: 1,
                  borderBottomEndRadius: 16,
                  borderBottomStartRadius: 16,
                  borderTopEndRadius: 16,
                  padding: 8,
                  marginTop: 4,
                }}
                labelField="label"
                valueField="value"
                onChange={(item) => {
                  setcreateForm({
                    ...createForm,
                    educational_level: item.value,
                  });
                }}
                value={createForm.educational_level}
                data={[
                  { label: "Primary", value: "primary" },
                  { label: "Secondary", value: "secondary" },
                  { label: "Higher Education Institute", value: "hei" },
                ]}
              />
            </View>

            <TouchableOpacity className="bg-primary mt-3 w-1/2 flex items-center justify-center rounded-2xl py-2">
              <Text className="text-white font-semibold text-lg">Create</Text>
            </TouchableOpacity>
            <View className="flex flex-col mt-7">
              <Text className="font-semibold">Are you a student?</Text>
              <Text className="mt-1">
                The current account is setup to be a teacher account. If you
                want to modify this, please contact support.
              </Text>
            </View>
          </View>
        ) : (
          <View className="w-full h-[95%] items-center mt-4 flex flex-col">
            {/* Top display */}
            <View className="border-y w-full flex flex-col px-5 py-3">
              <Text className="text-2xl font-bold">
                Mr Cawson's Chemistry Class
              </Text>
              <Text className="text-base font-light">Gareth Cawson</Text>
              <View className="flex flex-row items-center mt-1">
                <View className="bg-primary rounded-full p-2 flex items-center justify-center">
                  <LucidePaperclip size={20} className="text-white" />
                </View>
                <Text className="ml-2 font-light">Class code: HGFKAS</Text>
              </View>
            </View>

            {/* Scrollable classroom timeline */}
            <ScrollView className="mt-5 px-4 w-full">
              {/* shared an article object */}
              <View className="border w-full p-2 flex flex-col mb-5 rounded-2xl">
                <View className="flex flex-row items-center">
                  <Image
                    source={{
                      uri: "https://island.edu.hk/wp-content/uploads/2023/05/IMG_7575-1-2-1-1.jpg",
                    }}
                    className="w-12 h-12 rounded-full"
                  />
                  <View className="flex flex-col ml-3">
                    <Text className="font-medium text-base">Gareth Cawson</Text>
                    <Text className="text-xs font-light">Today at 09:55</Text>
                  </View>
                </View>
                <Text className="my-3">Shared an article:</Text>
                <TouchableOpacity className="border border-dashed w-full p-2 rounded-2xl flex flex-row">
                  <View className="bg-primary rounded-full p-2 flex items-center justify-center mr-3">
                    <LucideRocket
                      fill="white"
                      size={20}
                      className="text-white"
                    />
                  </View>
                  <View className="flex flex-col">
                    <Text className="text-sm font-bold flex-shrink w-1/2">
                      The chemistry involved in the APEP NASA Mission: 10
                      Mindblowing Facts
                    </Text>
                    <Text>5-minute read</Text>
                  </View>
                </TouchableOpacity>
              </View>

              {/* set an assignment object */}
              <View className="border w-full p-2 flex flex-col mb-5 rounded-2xl">
                <View className="flex flex-row items-center">
                  <Image
                    source={{
                      uri: "https://island.edu.hk/wp-content/uploads/2023/05/IMG_7575-1-2-1-1.jpg",
                    }}
                    className="w-12 h-12 rounded-full"
                  />
                  <View className="flex flex-col ml-3">
                    <Text className="font-medium text-base">Gareth Cawson</Text>
                    <Text className="text-xs font-light">
                      04/06 10:30 (Edited)
                    </Text>
                  </View>
                </View>
                <Text className="mt-3 ">Set an assignment:</Text>
                <View className="flex flex-row items-center">
                  <View className="bg-primary rounded-full p-2 flex items-center justify-center mr-2">
                    <LucideBookOpen
                      fill="white"
                      size={14}
                      className="text-white"
                    />
                  </View>
                  <Text>Read 5 articles</Text>
                </View>
                <View className="flex flex-row mt-3">
                  <TouchableOpacity className="border py-2 px-3 rounded-2xl">
                    <Text className="text-primary font-bold">View</Text>
                  </TouchableOpacity>
                  <View className="flex flex-row ml-3 items-center">
                    <View className="bg-green-400 p-0.5 rounded-full">
                      <LucideCheck size={20} className="text-black" />
                    </View>
                    <Text className="ml-2">This task is graded</Text>
                  </View>
                </View>
              </View>
            </ScrollView>
          </View>
        )}
      </SafeAreaView>
    );
  }
};

export default Education;
