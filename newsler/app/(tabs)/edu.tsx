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
  LucideChevronLeft,
  LucidePaperclip,
  LucidePlus,
  LucideRocket,
  LucideSearch,
  LucideSend,
  LucideX,
} from "lucide-react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { Dropdown } from "react-native-element-dropdown";
import Toast from "react-native-toast-message";
import { router } from "expo-router";

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
  const [reload, setreload] = useState(false);
  const [addMoreClassrooms, setaddMoreClassrooms] = useState(false);

  const randomTailwindColour = () => {
    const colors = [
      "red",
      "pink",
      "purple",
      "deep-purple",
      "indigo",
      "blue",
      "light-blue",
      "cyan",
      "teal",
      "green",
      "light-green",
      "lime",
      "yellow",
      "amber",
      "orange",
      "deep-orange",
      "grey",
    ];

    const randomIndex = Math.floor(Math.random() * colors.length);
    const randomColor = colors[randomIndex];

    return `bg-${randomColor}-400`;
  };

  const joinClassroom = async () => {
    if (joinform.classroom_code == "") {
      Toast.show({
        type: "error",
        text1: "Error",
        text2: "Incomplete fields",
        visibilityTime: 1000,
      });
      return;
    }

    try {
      Toast.show({
        type: "info",
        text1: "Joining classroom...",
        visibilityTime: 100000,
      });
      let reloading = true;
      while (reloading) {
        const response = await fetch(apiUrl + "/edu/classroom/join", {
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            Authorization:
              "Bearer " + (await AsyncStorage.getItem("session_token")),
          },
          body: JSON.stringify({
            user_id: await AsyncStorage.getItem("userId"),
            join_code: joinform.classroom_code,
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

          setjoinForm({
            classroom_code: "",
          });
          await AsyncStorage.setItem("session_token", content["session_token"]);
          await AsyncStorage.setItem("email", content["email"]);
          continue;
        }
        const responseJson = await response.json();
        Toast.show({
          type: "info",
          text1: "Joined classroom",
          visibilityTime: 500,
        });
        reloading = false;
        setreload(true);
      }
    } catch (e) {
      Toast.show({
        type: "error",
        text1: "Error",
        text2: "Classroom already joined (failed to join classroom)",
        visibilityTime: 1000,
      });
    }
  };

  const createClassroom = async () => {
    if (
      createForm.classroom_name == "" ||
      createForm.subject_code == "" ||
      createForm.educational_level == ""
    ) {
      Toast.show({
        type: "error",
        text1: "Error",
        text2: "Incomplete fields",
        visibilityTime: 1000,
      });
      return;
    }

    try {
      let reloading = true;
      while (reloading) {
        const response = await fetch(apiUrl + "/edu/classroom/create", {
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            Authorization:
              "Bearer " + (await AsyncStorage.getItem("session_token")),
          },
          body: JSON.stringify({
            user_id: await AsyncStorage.getItem("userId"),
            classroom_name: createForm.classroom_name,
            educational_level: createForm.educational_level,
            subject_code: createForm.subject_code,
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
          await AsyncStorage.setItem("session_token", content["session_token"]);
          await AsyncStorage.setItem("email", content["email"]);
          continue;
        }
        const responseJson = await response.json();
        reloading = false;
        setreload(true);
      }
    } catch (e) {
      Toast.show({
        type: "error",
        text1: "Error",
        visibilityTime: 1000,
      });
    }
  };

  useEffect(() => {
    if (!reload) {
      return;
    }
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
            await AsyncStorage.setItem("email", content["email"]);
            continue;
          }
          loading = false;
          const responseJson = await response.json();
          setClassroomList(responseJson["classrooms"]);
          setUserType(responseJson["edu_type"]);
          setisLoading(false);
          setreload(false);
        }
      } catch {}
    };

    fetchData();
  }, [reload]);

  useEffect(() => {
    setreload(true);
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
        {(classroomList.length == 0 || addMoreClassrooms) &&
        userType == "student" ? (
          <View className="w-full h-[95%] items-center justify-center flex px-6">
            {addMoreClassrooms ? (
              <TouchableOpacity
                className="absolute top-7 left-3"
                onPress={() => setaddMoreClassrooms(false)}
              >
                <LucideX size={28} className="text-black" />
              </TouchableOpacity>
            ) : (
              <></>
            )}
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
            <TouchableOpacity
              onPress={joinClassroom}
              className="bg-primary mt-3 w-1/2 flex items-center justify-center rounded-2xl py-2"
            >
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
        ) : (classroomList.length == 0 || addMoreClassrooms) &&
          userType == "teacher" ? (
          // if no classrooms in user list and type is teacher

          <View className="w-full h-[95%] items-center justify-center flex px-6">
            {addMoreClassrooms ? (
              <TouchableOpacity
                className="absolute top-7 left-3"
                onPress={() => setaddMoreClassrooms(false)}
              >
                <LucideX size={28} className="text-black" />
              </TouchableOpacity>
            ) : (
              <></>
            )}
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

            <TouchableOpacity
              onPress={createClassroom}
              className="bg-primary mt-3 w-1/2 flex items-center justify-center rounded-2xl py-2"
            >
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
            <View className="border-y w-full flex flex-row px-5 py-3 items-center">
              <View className="flex flex-col">
                <Text className="text-2xl font-bold">Classrooms</Text>
                <Text className="text-lg font-light">You are a {userType}</Text>
              </View>
              <TouchableOpacity
                className="ml-auto"
                onPress={() => setaddMoreClassrooms(true)}
              >
                <LucidePlus className="text-primary" />
              </TouchableOpacity>
            </View>

            <ScrollView className="mt-5 px-4 w-full">
              {classroomList.map((_, index) => (
                <TouchableOpacity
                  key={index}
                  className="w-full flex flex-col justify-center bg-secondary rounded-2xl p-3"
                  onPress={() =>
                    router.push(
                      "/classroom?classroom_id=" +
                        classroomList[index]["classroom_id"],
                    )
                  }
                >
                  <Text className="text-lg font-semibold">
                    {classroomList[index]["name"]}
                  </Text>
                  <Text className="font-light">
                    {classroomList[index]["subject_code"]} (
                    {classroomList[index]["education_level"]})
                  </Text>
                  <Text className="pt-3">
                    Teacher: {classroomList[index]["teacher"]}
                  </Text>
                </TouchableOpacity>
              ))}
            </ScrollView>
          </View>
        )}
      </SafeAreaView>
    );
  }
};

export default Education;
