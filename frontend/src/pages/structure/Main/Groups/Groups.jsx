import { Typography, Box, Container, Grid } from "@mui/material";
import React, { useEffect, } from "react";
import useCrud from "../../../../services/useCrud";
import { useParams } from "react-router-dom";
import GroupCard from "./GroupCard";
import GroupDetailsCard from "./GroupDetailsCard";

function Groups() {
  const { groupId } = useParams();
  const url = groupId ? `/groups/${groupId}/` : "/groups/";

  const { apiData, fetchData } = useCrud([], url);

  useEffect(() => {
    fetchData();
  }, [groupId]);

  useEffect(() => {
    console.log("Group ID:", apiData, "data test in GroupsComp");
  }, [groupId]);

  // Sample static data for groups

  // const staticData = [
  //   { id: 1, name: "Group 1" },
  //   { id: 2, name: "Group 2" },
  //   { id: 3, name: "Group 3" },
  // ];

  // const renderGroupList = () => {
  //   return (
  //     <Grid
  //       container
  //       spacing={{ xs: 2, sm: 3, md: 4, lg: 5 }}
  //       style={{ width: "100%" }}
  //     >
  //       {groups.map((group) => (
  //         <Grid
  //           item
  //           key={group.id}
  //           xs={12}
  //           sm={6}
  //           md={4}
  //           lg={3}
  //           xl={2}
  //           style={{ width: "100%" }}
  //         >
  //           {group.name}
  //         </Grid>
  //       ))}
  //     </Grid>
  //   );
  // };

  // const renderHeader = () => {
  //   if (groupId) {
  //     return null;
  //   } else {
  //     return (
  //       <Typography
  //         variant="h3"
  //         noWrap
  //         component="h1"
  //         sx={{
  //           display: {
  //             sm: "block",
  //             fontWeight: 700,
  //             fontSize: "48px",
  //             letterSpacing: "-2px",
  //           },
  //           textAlign: { xs: "center", sm: "left" },
  //         }}
  //       >
  //         All Groups
  //       </Typography>
  //     );
  //   }
  // };

  const renderHeader = () => {
    if (groupId) {
      return null;
    } else {
      return (
        <Typography
          variant="h3"
          noWrap
          component="h1"
          sx={{
            display: {
              sm: "block",
              fontWeight: 700,
              fontSize: "48px",
              letterSpacing: "-2px",
            },
            textAlign: { xs: "center", sm: "left" },
          }}
        >
          Active Groups
        </Typography>
      );
    }
  };

  const renderGroupList = () => {
    if (groupId) {
      return null;
    } else {
      return (
        <Grid
          container
          spacing={{ xs: 2, sm: 3, md: 4, lg: 5 }}
          style={{ width: "100%" }}
        >
          {Array.isArray(apiData) &&
            apiData.map((group) => (
              <Grid
                item
                key={group.id}
                xs={12}
                sm={6}
                md={4}
                lg={3}
                xl={2}
                style={{ width: "100%" }}
              >
                <GroupCard group={group} />
              </Grid>
            ))}
        </Grid>
      );
    }
  };

  const renderSubheader = () => {
    if (groupId) {
      return (
        <Box display="flex" justifyContent="center" alignItems="center">
          <GroupDetailsCard apiData={apiData} />
        </Box>
      );
    } else {
      return (
        <Typography
          variant="h6"
          noWrap
          component="h2"
          color="textSecondary"
          sx={{
            display: {
              sm: "block",
              fontWeight: 700,
              fontSize: "48px",
              letterSpacing: "-.5px",
            },
            textAlign: { xs: "center", sm: "left" },
            paddingBottom: 1,
          }}
        >
          Groups
        </Typography>
      );
    }
  };

  return (
    <>
      <Container maxWidth="xxl" sx={{ px: { md: 5, lg: 7 }, width: "100%" }}>
        <Box sx={{ pt: 4 }}>{renderHeader()}</Box>
        <Box>{renderSubheader()}</Box>
        <Box>{renderGroupList()}</Box>
      </Container>
    </>
  );
}

export default Groups;
