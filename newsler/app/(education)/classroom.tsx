import AsyncStorage from "@react-native-async-storage/async-storage";
import { useIsFocused } from "@react-navigation/native";
import { Dialog, Switch } from "@rneui/themed";
import { router, useFocusEffect } from "expo-router";
import { useSearchParams } from "expo-router/build/hooks";
import {
  LucideBookOpen,
  LucideCheck,
  LucideChevronLeft,
  LucidePaperclip,
  LucidePlus,
  LucideRocket,
  LucideX,
} from "lucide-react-native";
import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  Image,
  SafeAreaView,
  StatusBar,
  ActivityIndicator,
  TextInput,
  Keyboard,
} from "react-native";
import Toast from "react-native-toast-message";

export default function Classroom() {
  const [searchParams] = useSearchParams();
  const [classroomPosts, setclassroomPosts] = useState([]);
  const [createAssignment, setCreateAssignment] = useState({
    title: "",
    description: "",
    graded: false,
    articles: [],
  });
  const isFocused = useIsFocused();
  const [createCasualPost, setCreateCasualPost] = useState({
    title: "",
    description: "",
    articles: [],
  });
  const [name, setname] = useState("");
  const [teacherName, setteacherName] = useState("");
  const classroomId = searchParams[1];
  const [subject_code, setsubject_code] = useState("");
  const [isLoading, setisLoading] = useState(true);
  const [userType, setuserType] = useState("student");
  const apiUrl = process.env.EXPO_PUBLIC_API_URL;
  const [createPost, setCreatePost] = useState("");
  const [modalOpen, setModalOpen] = useState(false);
  const [selectModalOpen, setSelectModalOpen] = useState(false);
  const [modalArticles, setmodalArticles] = useState([]);
  const [isReloading, setisReloading] = useState(true);
  const [joinCode, setJoinCode] = useState("");

  useFocusEffect(
    React.useCallback(() => {
      setisReloading(true);
    }, []),
  );

  const createPostAction = async () => {
    try {
      let reloading = true;
      while (reloading) {
        if (createPost == "") {
          Toast.show({
            type: "error",
            text1: "Incomplete fields",
            visibilityTime: 1000,
          });
          reloading = false;
          return;
        }
        if (createPost == "share") {
          if (createCasualPost.articles.length == 0) {
            Toast.show({
              type: "error",
              text1: "Incomplete fields",
              visibilityTime: 1000,
            });
            reloading = false;
            return;
          }
        }
        Toast.show({
          type: "info",
          text1: "Posting post",
          visibilityTime: 100000,
        });
        const response = await fetch(apiUrl + "/edu/assignment/create", {
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            Authorization:
              "Bearer " + (await AsyncStorage.getItem("session_token")),
          },
          body: JSON.stringify({
            user_id: await AsyncStorage.getItem("userId"),
            assignment_type: createPost,
            articles: createCasualPost.articles,
            classroom_id: classroomId,
            description: createCasualPost.description,
            graded: false,
            title: createCasualPost.title,
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
        Toast.show({
          type: "info",
          text1: "Posted",
          visibilityTime: 500,
        });
        setCreatePost("");
        setisReloading(true);
        setCreateCasualPost({
          title: "",
          description: "",
          articles: [],
        });
      }
    } catch (e) {
      Toast.show({
        type: "error",
        text1: "An error occurred",
      });
    }
  };

  const createAssignmentAction = async () => {
    try {
      let reloading = true;
      while (reloading) {
        if (createPost == "") {
          Toast.show({
            type: "error",
            text1: "Incomplete fields",
            visibilityTime: 1000,
          });
          reloading = false;
          return;
        }
        if (createPost == "task") {
          if (
            createAssignment.articles.length == 0 ||
            createAssignment.title == "" ||
            createAssignment.description == ""
          ) {
            Toast.show({
              type: "error",
              text1: "Incomplete fields",
              visibilityTime: 1000,
            });
            reloading = false;
            return;
          }
        }
        Toast.show({
          type: "info",
          text1: "Posting assignment",
          visibilityTime: 100000,
        });
        const response = await fetch(apiUrl + "/edu/assignment/create", {
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            Authorization:
              "Bearer " + (await AsyncStorage.getItem("session_token")),
          },
          body: JSON.stringify({
            author_id: await AsyncStorage.getItem("userId"),
            assignment_type: createPost,
            articles: createAssignment.articles,
            classroom_id: classroomId,
            description: createAssignment.description,
            graded: createAssignment.graded,
            title: createAssignment.title,
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
        Toast.show({
          type: "info",
          text1: "Posted",
          visibilityTime: 500,
        });
        setCreatePost("");
        setisReloading(true);
        setCreateAssignment({
          title: "",
          description: "",
          graded: false,
          articles: [],
        });
      }
    } catch (e) {
      Toast.show({
        type: "error",
        text1: "An error occurred",
      });
    }
  };

  const toggleSelectModal = () => {
    setSelectModalOpen(!selectModalOpen);
  };

  const toggleModal = async () => {
    setModalOpen(!modalOpen);
    if (!modalOpen) {
      if (modalArticles.length != 0) {
        return;
      }
      setmodalArticles([]);
      try {
        let reloading = true;
        while (reloading) {
          const response = await fetch(apiUrl + "/edu/assignment/5mrv", {
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
          const responseJson = await response.json();
          reloading = false;

          setmodalArticles(responseJson);
        }
      } catch (e) {
        Toast.show({
          type: "error",
          text1: "An error occurred",
        });
      }
    }
  };

  const toggleSwitch = () => {
    setCreateAssignment({
      ...createAssignment,
      graded: !createAssignment.graded,
    });
  };

  const back = () => {
    router.back();
  };

  useEffect(() => {
    setisReloading(true);
  }, []);

  useEffect(() => {
    if (!isReloading) {
      return;
    }
    const fetchData = async () => {
      try {
        setisLoading(true);
        let reloading = true;
        while (reloading) {
          const response = await fetch(apiUrl + "/edu/classroom/load", {
            method: "POST",
            headers: {
              Accept: "application/json",
              "Content-Type": "application/json",
              Authorization:
                "Bearer " + (await AsyncStorage.getItem("session_token")),
            },
            body: JSON.stringify({
              classroom_id: classroomId,
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
          const responseJson = await response.json();
          reloading = false;

          setname(responseJson["details"]["name"]);
          setsubject_code(responseJson["details"]["subject_code"]);

          setuserType(responseJson["user_type"]);
          setclassroomPosts(responseJson["assignments"]);
          setteacherName(responseJson["details"]["teacher"]);
          setJoinCode(responseJson["details"]["join_code"]);
          setisLoading(false);
          setisReloading(false);
        }
      } catch (e) {
        Toast.show({
          type: "error",
          text1: "An error occurred",
        });
      }
    };
    fetchData();
  }, [isReloading]);

  if (isLoading) {
    return (
      <SafeAreaView
        className="bg-white h-full w-full"
        style={{ flex: 1, paddingTop: StatusBar.currentHeight }}
      >
        <View className="w-full h-full flex justify-center items-center">
          <TouchableOpacity className="absolute top-7 left-3" onPress={back}>
            <LucideChevronLeft size={28} className="text-black" />
          </TouchableOpacity>
          <ActivityIndicator color="black" className="mb-3" />
        </View>
      </SafeAreaView>
    );
  } else if (createPost == "share") {
    return (
      <SafeAreaView
        className="bg-white h-full w-full"
        style={{ flex: 1, paddingTop: StatusBar.currentHeight }}
      >
        <TouchableOpacity
          onPress={() => Keyboard.dismiss()}
          activeOpacity={1}
          className="w-full h-[95%] items-center justify-center flex px-6"
        >
          <TouchableOpacity
            className="absolute top-7 left-3"
            onPress={() => {
              setCreatePost("");
              setCreateCasualPost({
                title: "",
                description: "",
                articles: [],
              });
            }}
          >
            <LucideX size={28} className="text-black" />
          </TouchableOpacity>
          <Text className="text-primary font-bold text-2xl w-full text-left">
            Create a post
          </Text>
          <View className="w-full mt-2">
            <Text className="text-gray-600 text-xs">Title</Text>
            <View className="border border-black w-full mt-1 h-10 bg-black-100 rounded-b-2xl rounded-tr-2xl focus:border-primary items-center flex flex-row">
              <TextInput
                className="text-black h-full px-4 items-center text-base flex justify-center"
                value={createCasualPost.title}
                onChangeText={(e: string) =>
                  setCreateCasualPost({ ...createCasualPost, title: e })
                }
                secureTextEntry={false}
                placeholder="Enter a title here"
                placeholderTextColor={"gray"}
              />
            </View>
          </View>
          <View className="w-full mt-2">
            <Text className="text-gray-600 text-xs">Description</Text>
            <View className="border border-black w-full mt-1 h-40 bg-black-100 rounded-b-2xl rounded-tr-2xl focus:border-primary items-center flex flex-row">
              <TextInput
                className="text-black h-full px-4 items-center text-base flex justify-center"
                value={createCasualPost.description}
                onChangeText={(e: string) =>
                  setCreateCasualPost({ ...createCasualPost, description: e })
                }
                secureTextEntry={false}
                placeholder="Enter a description here"
                placeholderTextColor={"gray"}
                multiline={true}
              />
            </View>
          </View>
          <View className="w-full mt-2">
            <Text className="text-gray-600 text-xs">Articles</Text>
            <TouchableOpacity
              onPress={() => toggleModal()}
              className="w-full mt-1 min-h-14 p-1 rounded-2xl border-dashed border items-center justify-center"
            >
              {createCasualPost.articles.length == 0 ? (
                <Text>Touch to upload articles</Text>
              ) : (
                <View className="flex flex-col">
                  {createCasualPost.articles.map((_, index) => (
                    <View
                      key={index}
                      className="flex flex-row items-center w-full px-1"
                    >
                      <Text className="py-1" numberOfLines={1}>
                        {modalArticles
                          .find(
                            (article) =>
                              article.article_id ===
                              createCasualPost.articles[index],
                          )
                          ?.title.replace("\n", "")}
                      </Text>
                    </View>
                  ))}
                </View>
              )}
            </TouchableOpacity>
          </View>
          <TouchableOpacity
            onPress={() => createPostAction()}
            className="bg-primary mt-3 w-1/2 flex items-center justify-center rounded-2xl py-2"
          >
            <Text className="text-white font-semibold text-lg">
              Create Post
            </Text>
          </TouchableOpacity>
        </TouchableOpacity>

        <Dialog isVisible={modalOpen} onBackdropPress={toggleModal}>
          <View className="flex flex-col w-full">
            {modalArticles.length == 0 ? (
              <ActivityIndicator color="black" className="mb-3" />
            ) : (
              <View className="flex flex-col w-full">
                <Text className="text-lg">
                  Choose from recently viewed articles:
                </Text>
                {modalArticles.map((_, index) => (
                  <TouchableOpacity
                    className={`w-full mt-3 h-20 p-2 rounded-2xl border-dashed border items-center justify-center ${
                      createCasualPost.articles.includes(
                        modalArticles[index].article_id,
                      )
                        ? "bg-gray-200"
                        : ""
                    }`}
                    key={index}
                    onPress={() => {
                      if (
                        !createCasualPost.articles.includes(
                          modalArticles[index].article_id,
                        )
                      ) {
                        createCasualPost.articles.push(
                          modalArticles[index].article_id,
                        );
                        Toast.show({
                          type: "info",
                          text1: "Article added",
                          visibilityTime: 1000,
                        });
                      } else {
                        var index1 = createCasualPost.articles.indexOf(
                          modalArticles[index].article_id,
                        );
                        if (index !== -1) {
                          createCasualPost.articles.splice(index1, 1);
                        }
                        Toast.show({
                          type: "info",
                          text1: "Article removed",
                          visibilityTime: 1000,
                        });
                      }
                      setCreateCasualPost({
                        ...createCasualPost,
                        articles: createCasualPost.articles,
                      });
                    }}
                  >
                    <Image
                      source={{ uri: modalArticles[index].image_uri }}
                      className="w-full h-full rounded-t-2xl"
                    />
                    <Text numberOfLines={1}>{modalArticles[index].title}</Text>
                  </TouchableOpacity>
                ))}
              </View>
            )}
          </View>
        </Dialog>
      </SafeAreaView>
    );
  } else if (createPost == "task") {
    return (
      <SafeAreaView
        className="bg-white h-full w-full"
        style={{ flex: 1, paddingTop: StatusBar.currentHeight }}
      >
        <TouchableOpacity
          onPress={() => Keyboard.dismiss()}
          className="w-full h-[95%] items-center justify-center flex px-6"
          activeOpacity={1}
        >
          <TouchableOpacity
            className="absolute top-7 left-3"
            onPress={() => {
              setCreatePost("");
              setCreateAssignment({
                title: "",
                description: "",
                graded: false,
                articles: [],
              });
            }}
          >
            <LucideX size={28} className="text-black" />
          </TouchableOpacity>
          <Text className="text-primary font-bold text-2xl w-full text-left">
            Create an assignment
          </Text>
          <View className="w-full mt-2">
            <Text className="text-gray-600 text-xs">Title</Text>
            <View className="border border-black w-full mt-1 h-10 bg-black-100 rounded-b-2xl rounded-tr-2xl focus:border-primary items-center flex flex-row">
              <TextInput
                className="text-black h-full px-4 items-center text-base flex justify-center"
                value={createAssignment.title}
                onChangeText={(e: string) =>
                  setCreateAssignment({ ...createAssignment, title: e })
                }
                secureTextEntry={false}
                placeholder="Enter a title here"
                placeholderTextColor={"gray"}
              />
            </View>
          </View>
          <View className="w-full mt-2">
            <Text className="text-gray-600 text-xs">Description</Text>
            <View className="border border-black w-full mt-1 h-40 bg-black-100 rounded-b-2xl rounded-tr-2xl focus:border-primary items-center flex flex-row">
              <TextInput
                className="text-black h-full px-4 items-center text-base flex justify-center"
                value={createAssignment.description}
                onChangeText={(e: string) =>
                  setCreateAssignment({ ...createAssignment, description: e })
                }
                secureTextEntry={false}
                placeholder="Enter a description here"
                placeholderTextColor={"gray"}
                multiline={true}
              />
            </View>
          </View>
          <View className="w-full mt-2">
            <Text className="text-gray-600 text-xs">Graded</Text>
            <Switch
              value={createAssignment.graded}
              onValueChange={toggleSwitch}
              trackColor={{ true: "#275f6f" }}
              className="mt-1"
            />
          </View>
          <View className="w-full mt-2">
            <Text className="text-gray-600 text-xs">Articles</Text>
            <TouchableOpacity
              onPress={() => toggleModal()}
              className="w-full mt-1 min-h-14 p-1 rounded-2xl border-dashed border items-center justify-center"
            >
              {createAssignment.articles.length == 0 ? (
                <Text>Touch to upload articles</Text>
              ) : (
                <View className="flex flex-col">
                  {createAssignment.articles.map((_, index) => (
                    <View
                      key={index}
                      className="flex flex-row items-center w-full px-1"
                    >
                      <Text className="py-1" numberOfLines={1}>
                        {modalArticles
                          .find(
                            (article) =>
                              article.article_id ===
                              createAssignment.articles[index],
                          )
                          ?.title.replace("\n", "")}
                      </Text>
                    </View>
                  ))}
                </View>
              )}
            </TouchableOpacity>
          </View>
          <TouchableOpacity
            onPress={() => createAssignmentAction()}
            className="bg-primary mt-3 w-1/2 flex items-center justify-center rounded-2xl py-2"
          >
            <Text className="text-white font-semibold text-lg">
              Create Assignment
            </Text>
          </TouchableOpacity>
        </TouchableOpacity>

        <Dialog isVisible={modalOpen} onBackdropPress={toggleModal}>
          <View className="flex flex-col w-full">
            {modalArticles.length == 0 ? (
              <ActivityIndicator color="black" className="mb-3" />
            ) : (
              <View className="flex flex-col w-full">
                <Text className="text-lg">
                  Choose from recently viewed articles:
                </Text>
                {modalArticles.map((_, index) => (
                  <TouchableOpacity
                    className={`w-full mt-3 h-20 p-2 rounded-2xl border-dashed border items-center justify-center ${
                      createAssignment.articles.includes(
                        modalArticles[index].article_id,
                      )
                        ? "bg-gray-200"
                        : ""
                    }`}
                    key={index}
                    onPress={() => {
                      if (
                        !createAssignment.articles.includes(
                          modalArticles[index].article_id,
                        )
                      ) {
                        createAssignment.articles.push(
                          modalArticles[index].article_id,
                        );
                        Toast.show({
                          type: "info",
                          text1: "Article added",
                          visibilityTime: 1000,
                        });
                      } else {
                        var index1 = createAssignment.articles.indexOf(
                          modalArticles[index].article_id,
                        );
                        if (index !== -1) {
                          createAssignment.articles.splice(index1, 1);
                        }
                        Toast.show({
                          type: "info",
                          text1: "Article removed",
                          visibilityTime: 1000,
                        });
                      }
                      setCreateAssignment({
                        ...createAssignment,
                        articles: createAssignment.articles,
                      });
                    }}
                  >
                    <Image
                      source={{ uri: modalArticles[index].image_uri }}
                      className="w-full h-full rounded-t-2xl"
                    />
                    <Text numberOfLines={1}>{modalArticles[index].title}</Text>
                  </TouchableOpacity>
                ))}
              </View>
            )}
          </View>
        </Dialog>
      </SafeAreaView>
    );
  } else {
    return (
      <SafeAreaView
        className="bg-white h-full w-full"
        style={{ flex: 1, paddingTop: StatusBar.currentHeight }}
      >
        <TouchableOpacity className="ml-2" onPress={back}>
          <LucideChevronLeft size={28} className="text-black" />
        </TouchableOpacity>
        <View className="w-full h-[95%] items-center mt-4 flex flex-col">
          {/* Top display */}

          <View className="border-y w-full flex flex-row px-5 py-3 items-center">
            <View className="w-[95%] flex flex-col">
              <Text className="text-2xl font-bold">{name}</Text>
              <Text className="text-lg font-bold">{subject_code}</Text>
              <Text className="text-base font-light">{teacherName}</Text>
              <View className="flex flex-row items-center mt-1">
                <View className="bg-primary rounded-full p-2 flex items-center justify-center">
                  <LucidePaperclip size={20} className="text-white" />
                </View>
                <Text className="ml-2 font-light w-5/6">
                  Class code: {joinCode}
                </Text>
              </View>
            </View>
            {userType == "teacher" ? (
              <TouchableOpacity
                className="ml-auto"
                onPress={() => {
                  toggleSelectModal();
                }}
              >
                <LucidePlus className="text-primary" />
              </TouchableOpacity>
            ) : (
              <></>
            )}
          </View>

          <Dialog
            isVisible={selectModalOpen}
            onBackdropPress={toggleSelectModal}
            className="h-max"
          >
            <Text className="text-center text-xl font-medium">
              Create post:
            </Text>
            <TouchableOpacity
              onPress={() => {
                setCreatePost("share");
                toggleSelectModal();
              }}
              className="w-full h-10 flex items-center justify-center border mt-2 rounded-2xl"
            >
              <Text className="text-primary font-bold">Share article</Text>
            </TouchableOpacity>
            <TouchableOpacity
              onPress={() => {
                setCreatePost("task");
                toggleSelectModal();
              }}
              className="w-full h-10 flex items-center justify-center border mt-2 rounded-2xl"
            >
              <Text className="text-primary font-bold">Set a task</Text>
            </TouchableOpacity>
          </Dialog>

          {/* Scrollable classroom timeline */}
          <ScrollView className="mt-5 px-4 w-full">
            {classroomPosts.map((_, index) => (
              <View
                key={index}
                className="border w-full p-2 flex flex-col mb-5 rounded-2xl"
              >
                {classroomPosts[index]["type"] == "share" ? (
                  <>
                    {/* shared an article object */}
                    <View className="flex flex-row items-center">
                      <Image
                        source={{
                          uri: "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png",
                        }}
                        className="w-12 h-12 rounded-full"
                      />
                      <View className="flex flex-col ml-3">
                        <Text className="font-medium text-base">
                          {teacherName}
                        </Text>
                        <Text className="text-xs font-light">
                          {new Date().toLocaleDateString() ==
                          new Date(
                            classroomPosts[index]["timestamp"] * 1000,
                          ).toLocaleDateString()
                            ? "Today"
                            : new Date(
                                classroomPosts[index]["timestamp"] * 1000,
                              ).toLocaleDateString()}
                          {" at "}
                          {new Date(
                            classroomPosts[index]["timestamp"] * 1000,
                          ).toLocaleTimeString()}
                        </Text>
                      </View>
                    </View>

                    <View className="my-3">
                      {classroomPosts[index]["title"] == "" &&
                      classroomPosts[index]["description"] == "" ? (
                        <Text>
                          Shared{" "}
                          {classroomPosts[index]["article"].length
                            ? "an article"
                            : "some articles"}
                          :
                        </Text>
                      ) : (
                        <></>
                      )}
                      {classroomPosts[index]["title"] != "" ? (
                        <Text className="text-lg font-medium">
                          {classroomPosts[index].title}
                        </Text>
                      ) : (
                        <></>
                      )}
                      {classroomPosts[index]["description"] != "" ? (
                        <Text>{classroomPosts[index].description}</Text>
                      ) : (
                        <></>
                      )}
                    </View>
                    {classroomPosts[index]["article"].map((_, index1) => (
                      <TouchableOpacity
                        key={index1}
                        className="border border-dashed w-full p-2 rounded-2xl flex flex-row mb-1"
                        onPress={() =>
                          router.push(
                            "/article/" +
                              classroomPosts[index]["article"][index1][
                                "article_id"
                              ],
                          )
                        }
                      >
                        <Image
                          source={{
                            uri: classroomPosts[index]["article"][index1][
                              "image_uri"
                            ],
                          }}
                          className="w-20 h-full rounded-2xl mr-3"
                        />
                        <View className="flex flex-col">
                          <Text className="text-sm font-bold flex-shrink w-1/2">
                            {classroomPosts[index]["article"][index1][
                              "title"
                            ].replace("\n", "")}
                          </Text>
                          <Text>
                            {classroomPosts[index]["article"][index1]["length"]}
                            -minute read
                          </Text>
                        </View>
                      </TouchableOpacity>
                    ))}
                  </>
                ) : (
                  <>
                    {/* set an assignment object */}
                    <View className="flex flex-row items-center">
                      <Image
                        source={{
                          uri: "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png",
                        }}
                        className="w-12 h-12 rounded-full"
                      />
                      <View className="flex flex-col ml-3">
                        <Text className="font-medium text-base">
                          {teacherName}
                        </Text>
                        <Text className="text-xs font-light">
                          {new Date().toLocaleDateString() ==
                          new Date(
                            classroomPosts[index]["timestamp"] * 1000,
                          ).toLocaleDateString()
                            ? "Today"
                            : new Date(
                                classroomPosts[index]["timestamp"] * 1000,
                              ).toLocaleDateString()}
                          {" at "}
                          {new Date(
                            classroomPosts[index]["timestamp"] * 1000,
                          ).toLocaleTimeString()}
                        </Text>
                      </View>
                    </View>

                    <View className="my-3">
                      {classroomPosts[index]["title"] == "" &&
                      classroomPosts[index]["description"] == "" ? (
                        <Text>Set an assignment:</Text>
                      ) : (
                        <></>
                      )}
                      {classroomPosts[index]["title"] != "" ? (
                        <Text className="text-lg font-medium">
                          {classroomPosts[index].title}
                        </Text>
                      ) : (
                        <></>
                      )}
                      {classroomPosts[index]["description"] != "" ? (
                        <Text>{classroomPosts[index].description}</Text>
                      ) : (
                        <></>
                      )}
                    </View>

                    <View className="flex flex-row items-center">
                      <View className="bg-primary rounded-full p-2 flex items-center justify-center mr-2">
                        <LucideBookOpen
                          fill="white"
                          size={14}
                          className="text-white"
                        />
                      </View>
                      <Text>
                        Read {classroomPosts[index]["article"].length} article
                        {classroomPosts[index]["article"].length > 1 ? "s" : ""}
                      </Text>
                    </View>
                    <View className="flex flex-row mt-3">
                      <TouchableOpacity
                        onPress={() =>
                          router.push(
                            "/assignment?assignment_id=" +
                              classroomPosts[index].assignment_id,
                          )
                        }
                        className="border py-2 px-3 rounded-2xl"
                      >
                        <Text className="text-primary font-bold">View</Text>
                      </TouchableOpacity>
                      <View className="flex flex-row ml-3 items-center">
                        <View
                          className={`${classroomPosts[index]["graded"] == 1 ? "bg-green-400" : "bg-red-700"} p-0.5 rounded-full`}
                        >
                          {classroomPosts[index]["graded"] == 1 ? (
                            <LucideCheck size={20} className="text-black" />
                          ) : (
                            <LucideX size={20} className="text-white" />
                          )}
                        </View>
                        <Text className="ml-2">
                          This task is{" "}
                          {classroomPosts[index]["graded"] == 1
                            ? "graded"
                            : "not graded"}
                        </Text>
                      </View>
                    </View>
                  </>
                )}
              </View>
            ))}
          </ScrollView>
        </View>
      </SafeAreaView>
    );
  }
}
