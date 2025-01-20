import AsyncStorage from "@react-native-async-storage/async-storage";
import { useIsFocused } from "@react-navigation/native";
import { Dialog } from "@rneui/themed";
import { router } from "expo-router";
import { useSearchParams } from "expo-router/build/hooks";
import {
  LucideBookOpenText,
  LucideCheck,
  LucideChevronLeft,
  LucidePaperclip,
  LucidePlus,
  LucideTrash2,
  LucideWallpaper,
  LucideX,
} from "lucide-react-native";
import { useEffect, useState } from "react";
import {
  ActivityIndicator,
  StatusBar,
  TouchableOpacity,
  View,
  Text,
  Image,
  ScrollView,
} from "react-native";
import { Dropdown } from "react-native-element-dropdown";
import { SafeAreaView } from "react-native-safe-area-context";
import Toast from "react-native-toast-message";

export default function Assignment() {
  const [searchParams] = useSearchParams();
  const [isLoading, setisLoading] = useState(true);
  const assignmentId = searchParams[1];
  const apiUrl = process.env.EXPO_PUBLIC_API_URL;
  const [students, setStudents] = useState([]);
  const [details, setDetails] = useState({
    author: "",
    title: "",
    description: "",
    assignment_type: "",
    graded: "",
    timestamp: "",
    completed: "",
    user_type: "",
  });
  const [articles, setArticles] = useState([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [quiz, setQuiz] = useState([]);
  const [quizAnswers, setquizAnswers] = useState(["", "", "", "", ""]);
  const [quizArticleId, setQuizArticleId] = useState("");

  const toggleModal = () => {
    setQuiz([]);
    setquizAnswers(["", "", "", "", ""]);
    setQuizArticleId("");
    setModalOpen(!modalOpen);
  };

  useEffect(() => {
    setisLoading(true);
  }, []);

  useEffect(() => {
    if (!isLoading) {
      return;
    }
    const fetchData = async () => {
      try {
        let reloading = true;
        while (reloading) {
          const response = await fetch(apiUrl + "/edu/assignment/load", {
            method: "POST",
            headers: {
              Accept: "application/json",
              "Content-Type": "application/json",
              Authorization:
                "Bearer " + (await AsyncStorage.getItem("session_token")),
            },
            body: JSON.stringify({
              assignment_id: assignmentId,
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
          setDetails(responseJson["detail"]);
          if (responseJson["students"]) {
            setStudents(responseJson["students"]);
          } else {
            if (responseJson["detail"]["assignment_type"] == "share") {
              Toast.show({
                type: "error",
                text1: "Couldn't display assignment",
                visibilityTime: 1000,
              });
              router.back();
            }

            setArticles(responseJson["articles"]);
          }
          setisLoading(false);
        }
      } catch (e) {
        Toast.show({
          type: "error",
          text1: "An error occurred",
        });
      }
    };
    fetchData();
  }, [isLoading]);

  if (isLoading) {
    return (
      <SafeAreaView
        className="bg-white h-full w-full"
        style={{ flex: 1, paddingTop: StatusBar.currentHeight }}
      >
        <View className="w-full h-full flex justify-center items-center">
          <TouchableOpacity
            className="absolute top-7 left-3"
            onPress={() => router.back()}
          >
            <LucideChevronLeft size={28} className="text-black" />
          </TouchableOpacity>
          <ActivityIndicator color="black" className="mb-3" />
        </View>
      </SafeAreaView>
    );
  } else {
    return (
      <SafeAreaView
        className="bg-white h-full w-full"
        style={{ flex: 1, paddingTop: StatusBar.currentHeight }}
      >
        <TouchableOpacity className="ml-2" onPress={() => router.back()}>
          <LucideChevronLeft size={28} className="text-black" />
        </TouchableOpacity>
        <View className="w-full h-[95%] items-center mt-4 flex flex-col">
          <View className="border-y w-full flex flex-row px-5 py-3 items-center">
            <View className="w-[85%] flex flex-col">
              <Text className="w-full text-2xl font-bold text-center">
                Assignment
              </Text>
              <View className="flex flex-row items-center mb-2">
                <Image
                  source={{
                    uri: "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png",
                  }}
                  className="w-8 h-8 rounded-full"
                />
                <Text className="text-base font-light ml-2">
                  Teacher: {details.author}
                </Text>
              </View>
              {details.title == "" ? (
                <></>
              ) : (
                <Text className="text-xl font-medium">{details.title}</Text>
              )}
              {details.description == "" ? (
                <></>
              ) : (
                <Text className="text-base font-light">
                  {details.description}
                </Text>
              )}
              {details.description == "" && details.title == "" ? (
                <Text className="text-xl font-medium">Set an assignment</Text>
              ) : (
                <></>
              )}

              <Text className="mt-2 font-light">
                {new Date().toLocaleDateString() ==
                new Date(details.timestamp * 1000).toLocaleDateString()
                  ? "Today"
                  : new Date(details.timestamp * 1000).toLocaleDateString()}
                {" at "}
                {new Date(details.timestamp * 1000).toLocaleTimeString()}
              </Text>

              <View className="flex flex-row items-center mt-1">
                <View className="bg-primary rounded-full p-2 flex items-center justify-center">
                  <LucideWallpaper size={20} className="text-white" />
                </View>
                <Text className="ml-2 font-light w-5/6">{assignmentId}</Text>
              </View>
              <View className="flex flex-row mt-1 items-center">
                <View
                  className={`${details.graded == 1 ? "bg-green-400" : "bg-red-700"} p-0.5 rounded-full`}
                >
                  {details.graded == 1 ? (
                    <LucideCheck size={20} className="text-black" />
                  ) : (
                    <LucideX size={20} className="text-white" />
                  )}
                </View>
                <Text className="ml-2">
                  This task is {details.graded == 1 ? "graded" : "not graded"}
                </Text>
              </View>
            </View>
            {details.user_type == "teacher" ? (
              <TouchableOpacity
                className="ml-auto border rounded-2xl px-1 py-2 flex flex-col items-center justify-center w-[15%]"
                onPress={async () => {
                  try {
                    Toast.show({
                      type: "info",
                      text1: "Deleting assignment",
                      visibilityTime: 100000,
                    });
                    let reloading = true;
                    while (reloading) {
                      const response = await fetch(
                        apiUrl + "/edu/assignment/delete",
                        {
                          method: "POST",
                          headers: {
                            Accept: "application/json",
                            "Content-Type": "application/json",
                            Authorization:
                              "Bearer " +
                              (await AsyncStorage.getItem("session_token")),
                          },
                          body: JSON.stringify({
                            assignment_id: assignmentId,
                            user_id: await AsyncStorage.getItem("userId"),
                          }),
                        },
                      );
                      if (response.status === 308) {
                        const newResponse = await fetch(
                          apiUrl + "/auth/refreshsession",
                          {
                            method: "POST",
                            headers: {
                              Accept: "application/json",
                              "Content-Type": "application/json",
                            },
                            body: JSON.stringify({
                              refresh_token:
                                await AsyncStorage.getItem("refresh_token"),
                              user_id: await AsyncStorage.getItem("userId"),
                            }),
                          },
                        );
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
                      Toast.show({
                        type: "info",
                        text1: "Deleted assignment",
                        visibilityTime: 500,
                      });
                      router.back();
                    }
                  } catch (e) {
                    Toast.show({
                      type: "error",
                      text1: "An error occurred",
                    });
                  }
                }}
              >
                <LucideTrash2 className="text-primary" />
                <Text className="text-center">Delete post</Text>
              </TouchableOpacity>
            ) : (
              <></>
            )}
          </View>
          {details.user_type == "teacher" ? (
            <>
              <Text className="text-xl mt-2 font-semibold">Students:</Text>
              {students.length == 0 ? (
                <Text>You have no students yet!</Text>
              ) : (
                <ScrollView className="h-full mt-2 px-4 w-full">
                  {students.map((_, index) => (
                    <View
                      key={"student_" + index}
                      className="flex flex-col w-full border border-dashed py-2 px-3 rounded-2xl justify-center mb-1"
                    >
                      <View className="flex flex-row items-center mb-2">
                        <Image
                          source={{
                            uri: "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png",
                          }}
                          className="w-8 h-8 rounded-full mr-2"
                        />
                        <Text className="font-medium">
                          {students[index]["username"]}
                        </Text>
                      </View>
                      <View className="flex flex-row items-center mb-1">
                        <Text>Started assignment: </Text>
                        <Text>{students[index]["started"] ? "✅" : "❌"}</Text>
                      </View>
                      <View className="flex flex-row items-center mb-1">
                        <Text>Completed assignment: </Text>
                        <Text>
                          {students[index]["completed"] ? "✅" : "❌"}
                        </Text>
                      </View>
                      {students[index]["completed"] ? (
                        <View className="flex flex-row items-center">
                          <Text>Score: {students[index]["score"]}/5</Text>
                        </View>
                      ) : (
                        <></>
                      )}
                    </View>
                  ))}
                </ScrollView>
              )}
            </>
          ) : (
            <></>
          )}
          {details.user_type == "student" ? (
            <ScrollView className="h-full mt-5 px-4 w-full">
              {articles.map((_, index) => (
                <View className="flex flex-row w-full">
                  <TouchableOpacity
                    key={"articles_" + index}
                    className="border border-dashed w-3/4 p-2 rounded-2xl flex flex-row mb-1"
                    onPress={() =>
                      router.push("/article/" + articles[index]["article_id"])
                    }
                  >
                    <Image
                      source={{
                        uri: articles[index]["image_uri"],
                      }}
                      className="w-20 h-full rounded-2xl mr-3"
                    />
                    <View className="flex flex-col w-1/2">
                      <Text className="text-sm font-bold flex-shrink mb-1">
                        {articles[index]["title"].replace("\n", "")}
                      </Text>
                      <Text>
                        {articles[index]["length"]}
                        -minute read
                      </Text>
                    </View>
                  </TouchableOpacity>
                  {details.completed ? (
                    <View className="border border-dashed ml-2 w-1/4 p-2 rounded-2xl flex flex-col mb-1 items-center justify-center">
                      <LucideCheck className="text-green-600" />
                      <Text>Completed!</Text>
                    </View>
                  ) : (
                    <TouchableOpacity
                      key={"_" + index}
                      className="border border-dashed ml-2 w-1/4 p-2 rounded-2xl flex flex-col mb-1 items-center justify-center"
                      onPress={async () => {
                        try {
                          let reloading = true;
                          while (reloading) {
                            Toast.show({
                              type: "info",
                              text1: "Starting quiz",
                              visibilityTime: 100000,
                            });
                            const response = await fetch(
                              apiUrl + "/edu/quiz/load",
                              {
                                method: "POST",
                                headers: {
                                  Accept: "application/json",
                                  "Content-Type": "application/json",
                                  Authorization:
                                    "Bearer " +
                                    (await AsyncStorage.getItem(
                                      "session_token",
                                    )),
                                },
                                body: JSON.stringify({
                                  assignment_id: assignmentId,
                                  user_id: await AsyncStorage.getItem("userId"),
                                  article_id: articles[index]["article_id"],
                                }),
                              },
                            );
                            if (response.status === 308) {
                              const newResponse = await fetch(
                                apiUrl + "/auth/refreshsession",
                                {
                                  method: "POST",
                                  headers: {
                                    Accept: "application/json",
                                    "Content-Type": "application/json",
                                  },
                                  body: JSON.stringify({
                                    refresh_token:
                                      await AsyncStorage.getItem(
                                        "refresh_token",
                                      ),
                                    user_id:
                                      await AsyncStorage.getItem("userId"),
                                  }),
                                },
                              );
                              const content = await newResponse.json();
                              await AsyncStorage.setItem(
                                "session_token",
                                content["session_token"],
                              );
                              await AsyncStorage.setItem(
                                "email",
                                content["email"],
                              );
                              continue;
                            }
                            const responseJson = await response.json();
                            toggleModal();
                            setQuiz(responseJson["quiz"]);
                            setQuizArticleId(articles[index]["article_id"]);
                            reloading = false;
                            Toast.show({
                              type: "info",
                              text1: "Started quiz",
                              visibilityTime: 500,
                            });
                          }
                        } catch (e) {
                          Toast.show({
                            type: "error",
                            text1: "An error occurred",
                          });
                        }
                      }}
                    >
                      <LucideBookOpenText className="text-primary" />
                      <Text>Start quiz</Text>
                    </TouchableOpacity>
                  )}
                </View>
              ))}
            </ScrollView>
          ) : (
            <></>
          )}
          <Dialog isVisible={modalOpen} onBackdropPress={toggleModal}>
            <Text className="text-xl font-semibold mb-3">
              Quiz for article:
            </Text>
            {quiz.map((_, index) => (
              <View key={"quiz_" + index} className="flex flex-col mb-2">
                <Text>{_["question"]}</Text>
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
                    quizAnswers[index] = item.value;
                    setquizAnswers(quizAnswers);
                  }}
                  value={quizAnswers[index]}
                  data={[
                    { label: _["choices"][0], value: "a" },
                    { label: _["choices"][1], value: "b" },
                    { label: _["choices"][2], value: "c" },
                    { label: _["choices"][3], value: "d" },
                  ]}
                />
              </View>
            ))}
            <TouchableOpacity
              className="items-center justify-center border py-2 px-3 rounded-2xl mt-1"
              onPress={async () => {
                for (let answer of quizAnswers) {
                  if (answer == "") {
                    Toast.show({
                      type: "error",
                      text1: "Unanswered questions",
                    });
                    return;
                  }
                }
                try {
                  setisLoading(true);
                  let reloading = true;
                  Toast.show({
                    type: "info",
                    text1: "Submitting quiz...",
                    visibilityTime: 100000,
                  });
                  while (reloading) {
                    const response = await fetch(apiUrl + "/edu/quiz/finish", {
                      method: "POST",
                      headers: {
                        Accept: "application/json",
                        "Content-Type": "application/json",
                        Authorization:
                          "Bearer " +
                          (await AsyncStorage.getItem("session_token")),
                      },
                      body: JSON.stringify({
                        assignment_id: assignmentId,
                        article_id: quizArticleId,
                        user_id: await AsyncStorage.getItem("userId"),
                        answers: JSON.stringify(quizAnswers),
                      }),
                    });
                    if (response.status === 308) {
                      const newResponse = await fetch(
                        apiUrl + "/auth/refreshsession",
                        {
                          method: "POST",
                          headers: {
                            Accept: "application/json",
                            "Content-Type": "application/json",
                          },
                          body: JSON.stringify({
                            refresh_token:
                              await AsyncStorage.getItem("refresh_token"),
                            user_id: await AsyncStorage.getItem("userId"),
                          }),
                        },
                      );
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
                    toggleModal();
                    setTimeout(() => setisLoading(true), 1500);
                    Toast.show({
                      type: "info",
                      text1:
                        "Congrats! You got " + responseJson["score"] + "/5",
                      visibilityTime: 3000,
                    });
                  }
                } catch (e) {
                  Toast.show({
                    type: "error",
                    text1: "An error occurred",
                  });
                }
              }}
            >
              <Text className="text-primary font-bold">Submit</Text>
            </TouchableOpacity>
          </Dialog>
        </View>
      </SafeAreaView>
    );
  }
}
